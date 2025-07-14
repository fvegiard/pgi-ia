#!/usr/bin/env python3
"""
PGI-IA Prerequisites Checker
Pipeline Francis - Point 5: Blocage automatique sur prérequis
"""

import subprocess
import sys
import os
import json
from datetime import datetime

class PrerequisitesChecker:
    def __init__(self):
        self.checks = []
        self.blockers = []
        self.warnings = []
        
    def check(self, name, condition, error_msg, is_blocker=True):
        """Execute a check and record result"""
        result = {
            'name': name,
            'status': 'PASS' if condition else 'FAIL',
            'error': error_msg if not condition else None,
            'is_blocker': is_blocker,
            'timestamp': datetime.now().isoformat()
        }
        
        self.checks.append(result)
        
        if not condition:
            if is_blocker:
                self.blockers.append(result)
            else:
                self.warnings.append(result)
                
        return condition
    
    def run_command(self, cmd):
        """Run command and return (success, output)"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            return False, str(e)
    
    def check_all(self):
        """Run all prerequisite checks"""
        print("🔍 PGI-IA PREREQUISITES CHECK - PIPELINE FRANCIS")
        print("=" * 50)
        
        # 1. Check Python version
        success, output = self.run_command("python3 --version")
        self.check(
            "Python 3.8+",
            success and "Python 3." in output,
            "Python 3.8+ required",
            is_blocker=True
        )
        
        # 2. Check Docker
        success, _ = self.run_command("docker --version")
        self.check(
            "Docker installed",
            success,
            "Docker is required for production deployment",
            is_blocker=True
        )
        
        # 3. Check Docker running
        success, _ = self.run_command("docker ps")
        self.check(
            "Docker daemon running",
            success,
            "Docker daemon must be running",
            is_blocker=True
        )
        
        # 4. Check critical Python packages
        packages = {
            'flask': True,
            'openai': True,
            'PyPDF2': True,
            'psycopg2-binary': True,  # Missing in current setup
            'redis': False,
            'pdf2image': False
        }
        
        # Check in venv first, then system
        venv_pip = "/root/dev/pgi-ia/venv/bin/pip"
        
        for pkg, is_critical in packages.items():
            # Try venv first
            success, _ = self.run_command(f"{venv_pip} show {pkg}")
            if not success:
                # Fallback to system pip
                success, _ = self.run_command(f"pip show {pkg}")
                
            self.check(
                f"Python package: {pkg}",
                success,
                f"{pkg} package not installed (checked venv and system)",
                is_blocker=is_critical
            )
        
        # 5. Check API keys
        env_file = "/root/dev/pgi-ia/.env"
        api_keys = {}
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        api_keys[key] = bool(value)
        
        self.check(
            "DeepSeek API key",
            api_keys.get('DEEPSEEK_API_KEY', False),
            "DEEPSEEK_API_KEY not configured",
            is_blocker=False
        )
        
        self.check(
            "Gemini API key",
            api_keys.get('GEMINI_API_KEY', False),
            "GEMINI_API_KEY not configured",
            is_blocker=False
        )
        
        # 6. Check ports availability
        critical_ports = {
            5000: "Flask API",
            5432: "PostgreSQL",
            6379: "Redis",
            8080: "Frontend"
        }
        
        for port, service in critical_ports.items():
            success, _ = self.run_command(f"ss -tln | grep -q :{port}")
            self.check(
                f"Port {port} ({service})",
                success,
                f"Port {port} not available for {service}",
                is_blocker=(port == 5000)  # Only Flask API is critical
            )
        
        # 7. Check file permissions
        critical_paths = [
            "/root/dev/pgi-ia/backend/main.py",
            "/root/dev/pgi-ia/pgi_ia.db"
        ]
        
        for path in critical_paths:
            self.check(
                f"File exists: {os.path.basename(path)}",
                os.path.exists(path),
                f"Critical file missing: {path}",
                is_blocker=True
            )
        
        # 8. Check database
        success, _ = self.run_command("sqlite3 /root/dev/pgi-ia/pgi_ia.db '.tables' 2>/dev/null")
        self.check(
            "SQLite database accessible",
            success,
            "Database not accessible",
            is_blocker=True
        )
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate detailed report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_checks': len(self.checks),
            'passed': len([c for c in self.checks if c['status'] == 'PASS']),
            'failed': len([c for c in self.checks if c['status'] == 'FAIL']),
            'blockers': len(self.blockers),
            'warnings': len(self.warnings),
            'can_proceed': len(self.blockers) == 0,
            'checks': self.checks,
            'blockers': self.blockers,
            'warnings': self.warnings
        }
        
        # Print summary
        print("\n📊 SUMMARY")
        print("-" * 30)
        print(f"Total checks: {report['total_checks']}")
        print(f"✅ Passed: {report['passed']}")
        print(f"❌ Failed: {report['failed']}")
        print(f"🚫 Blockers: {report['blockers']}")
        print(f"⚠️  Warnings: {report['warnings']}")
        
        if report['blockers']:
            print("\n🚫 BLOCKING ISSUES:")
            for blocker in report['blockers']:
                print(f"  - {blocker['name']}: {blocker['error']}")
                
        if report['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in report['warnings']:
                print(f"  - {warning['name']}: {warning['error']}")
        
        print("\n🎯 VERDICT:", "✅ CAN PROCEED" if report['can_proceed'] else "❌ CANNOT PROCEED")
        
        # Save report
        report_file = f"/mnt/c/Users/fvegi/pgi_ia_prereqs_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Full report saved to: {report_file}")
        
        return report

if __name__ == "__main__":
    checker = PrerequisitesChecker()
    report = checker.check_all()
    
    # Exit with error code if blockers found
    sys.exit(0 if report['can_proceed'] else 1)