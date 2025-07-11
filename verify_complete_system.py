#!/usr/bin/env python3
"""
VÉRIFICATION COMPLÈTE DU SYSTÈME PGI-IA
Vérification de tous les outils, APIs, et dépendances
Mission: Tout doit fonctionner sans erreur
"""

import os
import sys
import json
import subprocess
import requests
import importlib
import logging
from pathlib import Path
from datetime import datetime
import pkg_resources

# Configuration
BASE_DIR = Path("/home/fvegi/dev/pgi-ia")
LOG_FILE = BASE_DIR / "system_verification.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class SystemVerifier:
    """Vérificateur complet du système PGI-IA"""
    
    def __init__(self):
        self.verification_results = {
            "apis": {},
            "tools": {},
            "dependencies": {},
            "services": {},
            "files": {},
            "system": {}
        }
        self.errors = []
        self.warnings = []
        
    def verify_system_basics(self):
        """Vérification des éléments de base du système"""
        print("🔧 VÉRIFICATION SYSTÈME DE BASE")
        print("=" * 50)
        
        # Python version
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            self.verification_results["system"]["python"] = True
        else:
            print(f"❌ Python version insuffisante: {python_version}")
            self.errors.append("Python version < 3.8")
            self.verification_results["system"]["python"] = False
            
        # GPU disponibilité
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            if result.returncode == 0:
                gpu_info = result.stdout.split('\n')[8:9]  # GPU info line
                print(f"✅ GPU détecté: {gpu_info[0] if gpu_info else 'NVIDIA GPU'}")
                self.verification_results["system"]["gpu"] = True
            else:
                print("❌ GPU NVIDIA non détecté")
                self.warnings.append("GPU NVIDIA non disponible")
                self.verification_results["system"]["gpu"] = False
        except FileNotFoundError:
            print("❌ nvidia-smi non trouvé")
            self.warnings.append("nvidia-smi non installé")
            self.verification_results["system"]["gpu"] = False
            
        # Mémoire système
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                total_mem = [line for line in meminfo.split('\n') if 'MemTotal' in line][0]
                mem_kb = int(total_mem.split()[1])
                mem_gb = mem_kb / (1024 * 1024)
                print(f"✅ Mémoire système: {mem_gb:.1f} GB")
                self.verification_results["system"]["memory"] = mem_gb
        except Exception as e:
            print(f"⚠️ Impossible de vérifier la mémoire: {e}")
            
    def verify_required_dependencies(self):
        """Vérification des dépendances Python requises"""
        print("\n📦 VÉRIFICATION DES DÉPENDANCES")
        print("=" * 50)
        
        required_packages = {
            # Core dependencies
            "torch": "PyTorch for deep learning",
            "transformers": "Hugging Face transformers",
            "datasets": "Hugging Face datasets",
            "peft": "Parameter-Efficient Fine-Tuning",
            "bitsandbytes": "Quantization support",
            
            # OCR and document processing
            "PyPDF2": "PDF text extraction",
            "PyMuPDF": "Advanced PDF processing (fitz)",
            "easyocr": "OCR capabilities",
            "opencv-python": "Computer vision (cv2)",
            "Pillow": "Image processing (PIL)",
            
            # Web and API
            "flask": "Web framework",
            "flask-cors": "CORS support",
            "requests": "HTTP requests",
            
            # Data processing
            "pandas": "Data manipulation",
            "numpy": "Numerical computing",
            "tqdm": "Progress bars",
            "pyyaml": "YAML configuration",
            
            # Additional tools
            "rich": "Terminal formatting",
            "psutil": "System monitoring"
        }
        
        missing_packages = []
        
        for package, description in required_packages.items():
            try:
                if package == "PyMuPDF":
                    import fitz
                    version = fitz.version[0]
                elif package == "opencv-python":
                    import cv2
                    version = cv2.__version__
                elif package == "Pillow":
                    from PIL import Image
                    version = "installed"
                else:
                    module = importlib.import_module(package.lower())
                    version = getattr(module, '__version__', 'unknown')
                
                print(f"✅ {package} v{version} - {description}")
                self.verification_results["dependencies"][package] = True
                
            except ImportError:
                print(f"❌ {package} MANQUANT - {description}")
                missing_packages.append(package)
                self.verification_results["dependencies"][package] = False
                self.errors.append(f"Dépendance manquante: {package}")
                
        # Auto-installation des packages manquants
        if missing_packages:
            print(f"\n🔧 INSTALLATION AUTOMATIQUE DES DÉPENDANCES MANQUANTES")
            self.install_missing_packages(missing_packages)
            
    def install_missing_packages(self, packages):
        """Installation automatique des packages manquants"""
        package_mapping = {
            "PyMuPDF": "PyMuPDF",
            "opencv-python": "opencv-python",
            "easyocr": "easyocr",
            "PyPDF2": "PyPDF2",
            "flask-cors": "flask-cors",
            "bitsandbytes": "bitsandbytes",
            "peft": "peft"
        }
        
        for package in packages:
            install_name = package_mapping.get(package, package.lower())
            try:
                print(f"📥 Installation de {package}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", install_name
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {package} installé avec succès")
                    self.verification_results["dependencies"][package] = True
                else:
                    print(f"❌ Échec installation {package}: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Erreur installation {package}: {e}")
                
    def verify_api_keys(self):
        """Vérification des clés API disponibles"""
        print("\n🔑 VÉRIFICATION DES CLÉS API")
        print("=" * 50)
        
        api_keys = {
            "OPENAI_API_KEY": "OpenAI GPT models",
            "DEEPSEEK_API_KEY": "DeepSeek models", 
            "ANTHROPIC_API_KEY": "Claude models",
            "GOOGLE_API_KEY": "Gemini models"
        }
        
        for key_name, description in api_keys.items():
            value = os.getenv(key_name)
            if value and len(value) > 10:
                masked_key = value[:8] + "..." + value[-4:]
                print(f"✅ {key_name}: {masked_key} - {description}")
                self.verification_results["apis"][key_name] = True
            else:
                print(f"❌ {key_name}: Non configurée - {description}")
                self.verification_results["apis"][key_name] = False
                self.warnings.append(f"Clé API manquante: {key_name}")
                
    def test_api_connections(self):
        """Test de connectivité des APIs"""
        print("\n🌐 TEST DE CONNECTIVITÉ DES APIS")
        print("=" * 50)
        
        # Test DeepSeek API
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            try:
                headers = {"Authorization": f"Bearer {deepseek_key}"}
                response = requests.get("https://api.deepseek.com/v1/models", headers=headers, timeout=10)
                if response.status_code == 200:
                    print("✅ DeepSeek API: Connexion réussie")
                    self.verification_results["apis"]["deepseek_connection"] = True
                else:
                    print(f"❌ DeepSeek API: Erreur {response.status_code}")
                    self.verification_results["apis"]["deepseek_connection"] = False
            except Exception as e:
                print(f"❌ DeepSeek API: Erreur connexion - {e}")
                self.verification_results["apis"]["deepseek_connection"] = False
        else:
            print("⚠️ DeepSeek API: Clé non configurée")
            
        # Test OpenAI API
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                headers = {"Authorization": f"Bearer {openai_key}"}
                response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
                if response.status_code == 200:
                    print("✅ OpenAI API: Connexion réussie")
                    self.verification_results["apis"]["openai_connection"] = True
                else:
                    print(f"❌ OpenAI API: Erreur {response.status_code}")
                    self.verification_results["apis"]["openai_connection"] = False
            except Exception as e:
                print(f"❌ OpenAI API: Erreur connexion - {e}")
                self.verification_results["apis"]["openai_connection"] = False
        else:
            print("⚠️ OpenAI API: Clé non configurée")
            
    def verify_project_structure(self):
        """Vérification de la structure du projet"""
        print("\n📁 VÉRIFICATION STRUCTURE PROJET")
        print("=" * 50)
        
        required_files = {
            # Core project files
            "backend/main.py": "Backend Flask principal",
            "backend/requirements.txt": "Dépendances backend",
            "frontend/index.html": "Interface utilisateur",
            "frontend/script.js": "JavaScript frontend",
            "config/agents.yaml": "Configuration multi-agents",
            
            # Training and AI
            "deepseek_training_dataset.jsonl": "Dataset d'entraînement",
            "train_deepseek_kahnawake_plans.py": "Script entraînement plans",
            "deepseek_finetune_english_complete.py": "Fine-tuning complet",
            
            # Audit scripts
            "audit_deepseek.py": "Audit technique DeepSeek",
            "audit_justina.py": "Audit UX Justina",
            
            # Documentation
            "README.md": "Documentation projet",
            "CLAUDE.md": "Configuration Claude"
        }
        
        for file_path, description in required_files.items():
            full_path = BASE_DIR / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"✅ {file_path} ({size} bytes) - {description}")
                self.verification_results["files"][file_path] = True
            else:
                print(f"❌ {file_path} - {description}")
                self.verification_results["files"][file_path] = False
                self.errors.append(f"Fichier manquant: {file_path}")
                
    def verify_services(self):
        """Vérification des services système"""
        print("\n🔧 VÉRIFICATION DES SERVICES")
        print("=" * 50)
        
        # Test Flask backend
        try:
            response = requests.get("http://localhost:5000/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend Flask: En cours d'exécution")
                self.verification_results["services"]["flask"] = True
            else:
                print(f"❌ Backend Flask: Erreur {response.status_code}")
                self.verification_results["services"]["flask"] = False
        except requests.exceptions.ConnectionError:
            print("⚠️ Backend Flask: Non démarré")
            self.verification_results["services"]["flask"] = False
            self.warnings.append("Backend Flask non démarré")
        except Exception as e:
            print(f"❌ Backend Flask: Erreur - {e}")
            self.verification_results["services"]["flask"] = False
            
    def verify_tools_availability(self):
        """Vérification des outils système disponibles"""
        print("\n🛠️ VÉRIFICATION DES OUTILS SYSTÈME")
        print("=" * 50)
        
        tools = {
            "git": "Contrôle de version",
            "python3": "Interpréteur Python",
            "pip": "Gestionnaire de packages",
            "nvidia-smi": "Monitoring GPU",
            "curl": "Client HTTP",
            "wget": "Téléchargement de fichiers"
        }
        
        for tool, description in tools.items():
            try:
                result = subprocess.run([tool, "--version"], capture_output=True)
                if result.returncode == 0:
                    print(f"✅ {tool}: Disponible - {description}")
                    self.verification_results["tools"][tool] = True
                else:
                    print(f"❌ {tool}: Non fonctionnel - {description}")
                    self.verification_results["tools"][tool] = False
            except FileNotFoundError:
                print(f"❌ {tool}: Non installé - {description}")
                self.verification_results["tools"][tool] = False
                self.errors.append(f"Outil manquant: {tool}")
                
    def create_missing_files(self):
        """Création des fichiers manquants critiques"""
        print("\n🔧 CRÉATION DES FICHIERS MANQUANTS")
        print("=" * 50)
        
        # requirements.txt pour backend
        requirements_path = BASE_DIR / "backend" / "requirements.txt"
        if not requirements_path.exists():
            requirements_content = """flask==2.3.3
flask-cors==4.0.0
torch>=2.0.0
transformers>=4.30.0
datasets>=2.12.0
peft>=0.4.0
bitsandbytes>=0.41.0
PyPDF2>=3.0.0
PyMuPDF>=1.23.0
easyocr>=1.7.0
opencv-python>=4.8.0
Pillow>=10.0.0
requests>=2.31.0
pyyaml>=6.0
tqdm>=4.65.0
pandas>=2.0.0
numpy>=1.24.0
psutil>=5.9.0
"""
            requirements_path.parent.mkdir(exist_ok=True)
            with open(requirements_path, 'w') as f:
                f.write(requirements_content)
            print(f"✅ Créé: {requirements_path}")
            
        # Configuration agents example
        agents_config_path = BASE_DIR / "config" / "agents.example.yaml"
        if not agents_config_path.exists():
            agents_config = """# Configuration Multi-Agents PGI-IA
agents:
  orchestrator:
    name: "Léa"
    type: "orchestrator"
    model: "gpt-4"
    api_key: "${OPENAI_API_KEY}"
    
  directive_agent:
    name: "DirectiveProcessor"
    type: "specialist"
    model: "deepseek-coder"
    api_key: "${DEEPSEEK_API_KEY}"
    
  analysis_agent:
    name: "TechnicalAnalyzer"
    type: "analyst"
    model: "claude-3"
    api_key: "${ANTHROPIC_API_KEY}"

settings:
  max_tokens: 2048
  temperature: 0.1
  timeout: 30
"""
            agents_config_path.parent.mkdir(exist_ok=True)
            with open(agents_config_path, 'w') as f:
                f.write(agents_config)
            print(f"✅ Créé: {agents_config_path}")
            
    def auto_fix_issues(self):
        """Correction automatique des problèmes détectés"""
        print("\n🔧 CORRECTION AUTOMATIQUE DES PROBLÈMES")
        print("=" * 50)
        
        # Création des répertoires manquants
        required_dirs = [
            "backend/agents",
            "frontend",
            "config", 
            "data",
            "logs",
            "plans_kahnawake",
            "plans_alexis_nihon",
            "deepseek_training_complete"
        ]
        
        for dir_path in required_dirs:
            full_path = BASE_DIR / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Répertoire créé: {dir_path}")
                
        # Création des fichiers manquants
        self.create_missing_files()
        
        # Installation des dépendances manquantes
        missing_deps = [pkg for pkg, status in self.verification_results["dependencies"].items() if not status]
        if missing_deps:
            print(f"🔧 Installation des dépendances manquantes: {missing_deps}")
            self.install_missing_packages(missing_deps)
            
    def generate_verification_report(self):
        """Génération du rapport de vérification"""
        print("\n📋 RAPPORT DE VÉRIFICATION SYSTÈME")
        print("=" * 60)
        
        total_checks = 0
        passed_checks = 0
        
        for category, items in self.verification_results.items():
            if isinstance(items, dict):
                for item, status in items.items():
                    total_checks += 1
                    if status:
                        passed_checks += 1
                        
        success_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"📊 TAUX DE RÉUSSITE: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
        print(f"❌ Erreurs: {len(self.errors)}")
        print(f"⚠️ Avertissements: {len(self.warnings)}")
        
        # Statut global
        if success_rate >= 90 and len(self.errors) == 0:
            print("🏆 STATUT: SYSTÈME PRÊT - Tout fonctionne parfaitement")
            system_status = "READY"
        elif success_rate >= 80 and len(self.errors) <= 2:
            print("✅ STATUT: SYSTÈME FONCTIONNEL - Corrections mineures requises")
            system_status = "FUNCTIONAL"
        elif success_rate >= 70:
            print("⚠️ STATUT: SYSTÈME PARTIEL - Corrections importantes requises")
            system_status = "PARTIAL"
        else:
            print("❌ STATUT: SYSTÈME DÉFAILLANT - Corrections critiques requises")
            system_status = "FAILED"
            
        # Sauvegarde du rapport
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_status": system_status,
            "success_rate": success_rate,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "verification_results": self.verification_results
        }
        
        report_path = BASE_DIR / "system_verification_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📁 Rapport sauvegardé: {report_path}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if self.errors:
            print("   🔧 Corriger les erreurs critiques listées")
        if self.warnings:
            print("   ⚠️ Examiner les avertissements")
        if system_status == "READY":
            print("   🚀 Système prêt pour l'entraînement DeepSeek")
            
        return system_status, success_rate

def main():
    """Fonction principale de vérification"""
    print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME PGI-IA")
    print("🎯 Mission: Tout doit fonctionner sans erreur")
    print("=" * 60)
    
    verifier = SystemVerifier()
    
    # Exécution de toutes les vérifications
    verifier.verify_system_basics()
    verifier.verify_required_dependencies()
    verifier.verify_api_keys()
    verifier.test_api_connections()
    verifier.verify_project_structure()
    verifier.verify_services()
    verifier.verify_tools_availability()
    
    # Correction automatique
    verifier.auto_fix_issues()
    
    # Rapport final
    system_status, success_rate = verifier.generate_verification_report()
    
    # Instructions finales
    if system_status == "READY":
        print(f"\n🎉 MISSION ACCOMPLIE!")
        print(f"   ✅ Système 100% fonctionnel")
        print(f"   🚀 Prêt pour l'entraînement DeepSeek")
        print(f"   📁 Logs: {LOG_FILE}")
    else:
        print(f"\n🔧 ACTIONS REQUISES:")
        if verifier.errors:
            print(f"   ❌ Résoudre {len(verifier.errors)} erreurs critiques")
        print(f"   📋 Voir rapport détaillé: system_verification_report.json")
        
    return system_status == "READY"

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)