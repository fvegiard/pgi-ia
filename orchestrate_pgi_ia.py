#!/usr/bin/env python3
"""
PGI-IA Orchestrator - Claude Code Expert System
Automatise complètement le démarrage et la gestion du système PGI-IA
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent
VENV_PATH = PROJECT_ROOT / "venv_pgi_ia"
PYTHON = VENV_PATH / "bin" / "python"
SUDO_PASSWORD = "12345"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PGI-IA-Orchestrator")

class PGIOrchestrator:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.status = {
            "backend": False,
            "deepseek": False,
            "gemini": False,
            "database": False,
            "gpu": False,
            "services": {}
        }
    
    def run_command(self, cmd, check=True, cwd=None, env=None):
        """Execute command with proper error handling"""
        if cwd is None:
            cwd = self.project_root
        
        logger.info(f"Executing: {cmd}")
        
        try:
            if isinstance(cmd, str):
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)
            
            if check and result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                return False, result.stderr
            
            return True, result.stdout
        except Exception as e:
            logger.error(f"Exception running command: {str(e)}")
            return False, str(e)
    
    def check_gpu(self):
        """Verify GPU availability"""
        logger.info("Checking GPU availability...")
        success, output = self.run_command("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader")
        
        if success:
            logger.info(f"GPU detected: {output.strip()}")
            self.status["gpu"] = True
            return True
        
        logger.warning("No GPU detected, will use CPU")
        return False
    
    def setup_environment(self):
        """Setup environment variables"""
        logger.info("Setting up environment...")
        
        # Load .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
                        logger.info(f"Set {key}")
        
        # Set additional environment variables
        os.environ["PROJECT_ROOT"] = str(self.project_root)
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        
        return True
    
    def setup_database(self):
        """Initialize or verify database"""
        logger.info("Setting up database...")
        
        db_path = self.project_root / "pgi_ia.db"
        if db_path.exists():
            logger.info("Database already exists")
            self.status["database"] = True
            return True
        
        # Create database
        cmd = f"{PYTHON} setup_database.py"
        success, output = self.run_command(cmd)
        
        if success:
            logger.info("Database created successfully")
            self.status["database"] = True
            return True
        
        logger.error("Failed to create database")
        return False
    
    def configure_apis(self):
        """Configure all available APIs"""
        logger.info("Configuring APIs...")
        
        # Check DeepSeek
        if os.getenv("DEEPSEEK_API_KEY"):
            logger.info("DeepSeek API configured")
            self.status["deepseek"] = True
        
        # Configure Gemini if needed
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            logger.info("Gemini API key not found, checking for free tier...")
            # Could implement auto-setup here
        else:
            self.status["gemini"] = True
        
        return True
    
    def start_backend(self):
        """Start Flask backend"""
        logger.info("Starting Flask backend...")
        
        # Kill any existing Flask process
        self.run_command("pkill -f 'python.*backend/main.py'", check=False)
        time.sleep(2)
        
        # Start Flask in background
        env = os.environ.copy()
        env["FLASK_APP"] = "backend.main"
        env["FLASK_ENV"] = "production"
        
        cmd = [str(PYTHON), "backend/main.py"]
        process = subprocess.Popen(cmd, cwd=self.project_root, env=env)
        
        # Wait for startup
        time.sleep(5)
        
        # Check if running
        success, output = self.run_command("curl -s http://localhost:5000/health")
        
        if success and "healthy" in output:
            logger.info("Backend started successfully")
            self.status["backend"] = True
            self.status["services"]["backend_pid"] = process.pid
            return True
        
        logger.error("Backend failed to start")
        return False
    
    def create_email_watcher(self):
        """Create email watcher service"""
        logger.info("Creating email watcher service...")
        
        email_watcher_code = '''#!/usr/bin/env python3
"""Email Watcher Service for PGI-IA"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path

# Pour Windows/Outlook
try:
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False

# Pour Linux/IMAP
import imaplib
import email
from email.header import decode_header

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmailWatcher")

class EmailWatcher:
    def __init__(self, backend_url="http://localhost:5000"):
        self.backend_url = backend_url
        self.processed_emails = set()
        
    def watch_outlook(self):
        """Watch Outlook emails on Windows"""
        if not OUTLOOK_AVAILABLE:
            logger.error("Outlook not available on this system")
            return
            
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6)
        
        logger.info("Watching Outlook inbox...")
        
        while True:
            for mail in inbox.Items:
                if mail.EntryID not in self.processed_emails:
                    if self.is_project_email(mail.Subject, mail.Body):
                        self.process_email({
                            "id": mail.EntryID,
                            "from": mail.SenderEmailAddress,
                            "subject": mail.Subject,
                            "body": mail.Body,
                            "attachments": [att.FileName for att in mail.Attachments],
                            "received": str(mail.ReceivedTime)
                        })
                        self.processed_emails.add(mail.EntryID)
            
            time.sleep(30)  # Check every 30 seconds
    
    def watch_imap(self, server, username, password):
        """Watch IMAP emails"""
        logger.info(f"Connecting to IMAP server {server}...")
        
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
        mail.select("inbox")
        
        while True:
            _, messages = mail.search(None, "UNSEEN")
            
            for num in messages[0].split():
                _, msg = mail.fetch(num, "(RFC822)")
                email_body = msg[0][1]
                email_message = email.message_from_bytes(email_body)
                
                subject = decode_header(email_message["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                if self.is_project_email(subject, ""):
                    self.process_email({
                        "id": num.decode(),
                        "from": email_message["From"],
                        "subject": subject,
                        "body": self.get_email_body(email_message),
                        "received": email_message["Date"]
                    })
            
            time.sleep(30)
    
    def is_project_email(self, subject, body):
        """Check if email is project-related"""
        keywords = ["plan", "électrique", "electrical", "dwg", "pdf", "kahnawake", "alexis-nihon"]
        text = (subject + " " + body).lower()
        return any(keyword in text for keyword in keywords)
    
    def process_email(self, email_data):
        """Send email to backend for processing"""
        logger.info(f"Processing email: {email_data['subject']}")
        
        import requests
        try:
            response = requests.post(
                f"{self.backend_url}/api/emails/process",
                json=email_data
            )
            if response.status_code == 200:
                logger.info("Email processed successfully")
            else:
                logger.error(f"Failed to process email: {response.text}")
        except Exception as e:
            logger.error(f"Error sending email to backend: {e}")
    
    def get_email_body(self, email_message):
        """Extract email body"""
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        return body

if __name__ == "__main__":
    watcher = EmailWatcher()
    
    # Try Outlook first (Windows)
    if OUTLOOK_AVAILABLE:
        watcher.watch_outlook()
    else:
        # Fallback to IMAP
        logger.info("Outlook not available, using IMAP mock mode")
        # In production, get credentials from environment
        # watcher.watch_imap("imap.gmail.com", "user@gmail.com", "password")
        
        # For now, just log
        logger.info("Email watcher in standby mode (no email server configured)")
        while True:
            time.sleep(60)
'''
        
        # Write email watcher
        watcher_path = self.project_root / "backend" / "workers" / "email_watcher.py"
        watcher_path.write_text(email_watcher_code)
        
        logger.info("Email watcher service created")
        return True
    
    def create_master_startup_script(self):
        """Create the ultimate startup script"""
        logger.info("Creating master startup script...")
        
        startup_script = '''#!/bin/bash
# PGI-IA Master Startup Script
# Starts everything automatically

echo "🚀 Starting PGI-IA System..."

# Activate virtual environment
source venv_pgi_ia/bin/activate

# Load environment variables
source setup_env.sh

# Start all services
echo "📦 Starting backend services..."
python orchestrate_pgi_ia.py

echo "🌐 Opening dashboard..."
if command -v xdg-open &> /dev/null; then
    xdg-open frontend/dashboard.html
elif command -v open &> /dev/null; then
    open frontend/dashboard.html
else
    echo "Please open frontend/dashboard.html in your browser"
fi

echo "✅ PGI-IA is ready!"
echo "Backend: http://localhost:5000"
echo "Dashboard: file://$(pwd)/frontend/dashboard.html"
'''
        
        script_path = self.project_root / "start_pgi_ia_auto.sh"
        script_path.write_text(startup_script)
        script_path.chmod(0o755)
        
        logger.info("Master startup script created")
        return True
    
    def fix_requirements(self):
        """Fix all dependency issues"""
        logger.info("Fixing requirements...")
        
        requirements = """Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
requests==2.31.0
Pillow==10.0.0
pytesseract==0.3.10
easyocr==1.7.0
PyPDF2==3.0.1
pdf2image==1.16.3
numpy<2.0.0
torch>=2.0.0
transformers>=4.30.0
deepspeed>=0.10.0
peft>=0.4.0
datasets>=2.14.0
accelerate>=0.21.0
sentencepiece>=0.1.99
colorama>=0.4.6
tqdm>=4.65.0
pypdfium2>=4.20.0
pymupdf>=1.23.0
python-multipart>=0.0.6
aiofiles>=23.2.1
sqlalchemy>=2.0.0
alembic>=1.12.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pywin32>=306; sys_platform == 'win32'
"""
        
        req_path = self.project_root / "requirements_fixed.txt"
        req_path.write_text(requirements)
        
        # Install with fixed numpy
        cmd = f"{VENV_PATH}/bin/pip install -r requirements_fixed.txt --upgrade"
        success, output = self.run_command(cmd)
        
        if success:
            logger.info("Requirements fixed successfully")
            return True
        
        logger.error("Failed to fix requirements")
        return False
    
    def create_docker_compose(self):
        """Create production-ready docker-compose"""
        logger.info("Creating Docker configuration...")
        
        dockerfile = '''FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    tesseract-ocr \\
    tesseract-ocr-fra \\
    poppler-utils \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    wget \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_fixed.txt .
RUN pip install --no-cache-dir -r requirements_fixed.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/drop_zone uploads

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "backend/main.py"]
'''
        
        docker_compose = '''version: '3.8'

services:
  backend:
    build: .
    container_name: pgi-ia-backend
    ports:
      - "5000:5000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: pgi-ia-nginx
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    restart: unless-stopped
'''
        
        # Write files
        (self.project_root / "Dockerfile").write_text(dockerfile)
        (self.project_root / "docker-compose.yml").write_text(docker_compose)
        
        logger.info("Docker configuration created")
        return True
    
    def generate_status_report(self):
        """Generate comprehensive status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": self.status,
            "health_check": {
                "backend": self.status["backend"],
                "database": self.status["database"],
                "gpu": self.status["gpu"],
                "apis": {
                    "deepseek": self.status["deepseek"],
                    "gemini": self.status["gemini"]
                }
            },
            "recommendations": []
        }
        
        # Add recommendations
        if not self.status["gpu"]:
            report["recommendations"].append("Consider using GPU for faster processing")
        
        if not self.status["gemini"]:
            report["recommendations"].append("Configure Gemini API for enhanced PDF analysis")
        
        # Write report
        report_path = self.project_root / "system_status_report.json"
        report_path.write_text(json.dumps(report, indent=2))
        
        logger.info(f"Status report generated: {report_path}")
        return report
    
    def orchestrate(self):
        """Main orchestration logic"""
        logger.info("=" * 50)
        logger.info("PGI-IA Orchestrator Starting...")
        logger.info("=" * 50)
        
        steps = [
            ("Environment Setup", self.setup_environment),
            ("GPU Check", self.check_gpu),
            ("Fix Requirements", self.fix_requirements),
            ("Database Setup", self.setup_database),
            ("API Configuration", self.configure_apis),
            ("Backend Startup", self.start_backend),
            ("Email Watcher Creation", self.create_email_watcher),
            ("Docker Setup", self.create_docker_compose),
            ("Master Script Creation", self.create_master_startup_script)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n>>> {step_name}")
            try:
                if not step_func():
                    logger.error(f"Failed at step: {step_name}")
                    # Continue anyway for maximum functionality
            except Exception as e:
                logger.error(f"Exception in {step_name}: {str(e)}")
        
        # Generate final report
        report = self.generate_status_report()
        
        logger.info("\n" + "=" * 50)
        logger.info("ORCHESTRATION COMPLETE")
        logger.info("=" * 50)
        logger.info(f"Backend: {'✅ Running' if self.status['backend'] else '❌ Failed'}")
        logger.info(f"Database: {'✅ Ready' if self.status['database'] else '❌ Failed'}")
        logger.info(f"GPU: {'✅ Available' if self.status['gpu'] else '⚠️ CPU Mode'}")
        logger.info(f"DeepSeek: {'✅ Configured' if self.status['deepseek'] else '❌ Missing'}")
        logger.info(f"Gemini: {'✅ Configured' if self.status['gemini'] else '⚠️ Not configured'}")
        logger.info("\nAccess the system at: http://localhost:5000")
        logger.info("Dashboard: file://" + str(self.project_root / "frontend" / "dashboard.html"))
        
        return report

if __name__ == "__main__":
    orchestrator = PGIOrchestrator()
    orchestrator.orchestrate()