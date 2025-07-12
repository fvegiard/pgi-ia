#!/usr/bin/env python3
"""
Vérification complète du système PGI-IA
Créé automatiquement pour faire l'état des lieux
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class SystemVerifier:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "summary": {
                "total_checks": 0,
                "passed": 0,
                "failed": 0
            }
        }
        
    def check_python_env(self):
        """Vérifier l'environnement Python"""
        print("\n🐍 Vérification Python...")
        try:
            version = sys.version
            self.report["checks"]["python"] = {
                "status": "OK",
                "version": version,
                "executable": sys.executable
            }
            print(f"✅ Python {sys.version.split()[0]} détecté")
            return True
        except Exception as e:
            self.report["checks"]["python"] = {"status": "FAILED", "error": str(e)}
            print(f"❌ Erreur Python: {e}")
            return False
            
    def check_structure(self):
        """Vérifier la structure du projet"""
        print("\n📁 Vérification structure...")
        required_dirs = ["backend", "frontend", "config", "data", "scripts", "tests"]
        missing = []
        
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                print(f"✅ /{dir_name} présent")
            else:
                print(f"❌ /{dir_name} manquant")
                missing.append(dir_name)
                
        self.report["checks"]["structure"] = {
            "status": "OK" if not missing else "PARTIAL",
            "missing_dirs": missing
        }
        return len(missing) == 0
        
    def check_files(self):
        """Vérifier les fichiers clés"""
        print("\n📄 Vérification fichiers...")
        
        # Scripts mentionnés dans CLAUDE.md
        expected_scripts = [
            "verify_complete_system.py",
            "audit_deepseek.py",
            "audit_justina.py", 
            "deepseek_finetune_english_complete.py",
            "start_all_services.py",
            "gemini_manager.py",
            "google_session_manager.py"
        ]
        
        missing_scripts = []
        for script in expected_scripts:
            if not (self.base_path / script).exists():
                missing_scripts.append(script)
                
        # Fichiers backend
        backend_files = [
            "backend/main.py",
            "backend/requirements.txt"
        ]
        
        backend_ok = all((self.base_path / f).exists() for f in backend_files)
        
        print(f"✅ Backend: {'Complet' if backend_ok else 'Partiel'}")
        print(f"❌ Scripts manquants: {len(missing_scripts)}/{len(expected_scripts)}")
        
        self.report["checks"]["files"] = {
            "status": "PARTIAL",
            "missing_scripts": missing_scripts,
            "backend_complete": backend_ok
        }
        return len(missing_scripts) == 0
        
    def check_apis(self):
        """Vérifier les clés API"""
        print("\n🔑 Vérification APIs...")
        api_status = {}
        
        api_keys = {
            "OPENAI_API_KEY": "OpenAI",
            "DEEPSEEK_API_KEY": "DeepSeek",
            "GEMINI_API_KEY": "Gemini",
            "ANTHROPIC_API_KEY": "Anthropic"
        }
        
        for env_var, name in api_keys.items():
            if os.environ.get(env_var):
                print(f"✅ {name}: Configurée")
                api_status[name] = "OK"
            else:
                print(f"❌ {name}: Non configurée")
                api_status[name] = "MISSING"
                
        self.report["checks"]["apis"] = api_status
        return all(status == "OK" for status in api_status.values())
        
    def check_dependencies(self):
        """Vérifier si les dépendances peuvent être installées"""
        print("\n📦 Vérification dépendances...")
        req_file = self.base_path / "backend" / "requirements.txt"
        
        if req_file.exists():
            print("✅ requirements.txt trouvé")
            self.report["checks"]["dependencies"] = {"status": "FILE_FOUND"}
            return True
        else:
            print("❌ requirements.txt manquant")
            self.report["checks"]["dependencies"] = {"status": "FILE_MISSING"}
            return False
            
    def generate_report(self):
        """Générer le rapport final"""
        print("\n" + "="*50)
        print("📊 RAPPORT FINAL")
        print("="*50)
        
        total = len(self.report["checks"])
        passed = sum(1 for check in self.report["checks"].values() 
                    if isinstance(check, dict) and check.get("status") in ["OK", "FILE_FOUND"])
        
        self.report["summary"] = {
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "percentage": round((passed / total) * 100, 1) if total > 0 else 0
        }
        
        print(f"\n✅ Tests réussis: {passed}/{total} ({self.report['summary']['percentage']}%)")
        print(f"❌ Tests échoués: {total - passed}/{total}")
        
        # Sauvegarder le rapport
        report_file = self.base_path / "system_verification_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\n💾 Rapport sauvé dans: {report_file}")
        
        return self.report
        
def main():
    print("🚀 Démarrage de la vérification système PGI-IA...")
    print(f"📍 Répertoire: {Path.cwd()}")
    
    verifier = SystemVerifier()
    
    # Exécuter les vérifications
    verifier.check_python_env()
    verifier.check_structure()
    verifier.check_files()
    verifier.check_apis()
    verifier.check_dependencies()
    
    # Générer le rapport
    report = verifier.generate_report()
    
    print("\n🔧 Prochaines étapes recommandées:")
    
    if report["checks"]["files"]["missing_scripts"]:
        print("\n1. Créer les scripts manquants ou mettre à jour la documentation")
        
    if any(status == "MISSING" for status in report["checks"].get("apis", {}).values()):
        print("\n2. Configurer les clés API manquantes dans .env ou variables d'environnement")
        
    print("\n3. Créer/activer l'environnement virtuel:")
    print("   python3 -m venv venv_pgi_ia")
    print("   source venv_pgi_ia/bin/activate")
    print("   pip install -r backend/requirements.txt")
    
    print("\n✨ Vérification terminée!")
    
if __name__ == "__main__":
    main()
