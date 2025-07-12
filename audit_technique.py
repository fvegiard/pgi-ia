"""
Audit Technique Complet PGI-IA v4.1
Analyse approfondie du système
"""
import os
import subprocess
import json
from datetime import datetime
import re

class TechnicalAuditor:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "version": "PGI-IA v4.1",
            "components": {},
            "api_status": {},
            "security": {},
            "performance": {}
        }
    
    def audit_backend(self):
        """Audit du backend Flask"""
        print("🔍 Audit Backend...")
        
        # Vérifier les endpoints
        try:
            import requests
            
            # Test des endpoints principaux
            endpoints = [
                ("http://localhost:5001/", "Root API"),
                ("http://localhost:5001/projects", "Projects"),
                ("http://localhost:5001/api/status", "Status"),
                ("http://localhost:5000/health", "Health (Docker)")
            ]
            
            backend_results = []
            for url, name in endpoints:
                try:
                    response = requests.get(url, timeout=2)
                    backend_results.append({
                        "endpoint": name,
                        "url": url,
                        "status": response.status_code,
                        "ok": response.status_code == 200
                    })
                except:
                    backend_results.append({
                        "endpoint": name,
                        "url": url,
                        "status": "offline",
                        "ok": False
                    })
            
            self.results["components"]["backend"] = backend_results
            
        except Exception as e:
            self.results["components"]["backend"] = {"error": str(e)}
    
    def audit_docker(self):
        """Audit des conteneurs Docker"""
        print("🐳 Audit Docker...")
        
        try:
            # Liste des conteneurs
            result = subprocess.run(
                ["docker", "ps", "--format", "json"],
                capture_output=True,
                text=True
            )
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    container = json.loads(line)
                    containers.append({
                        "name": container.get("Names"),
                        "image": container.get("Image"),
                        "status": container.get("Status"),
                        "ports": container.get("Ports")
                    })
            
            self.results["components"]["docker"] = {
                "active": len(containers),
                "containers": containers
            }
            
        except Exception as e:
            self.results["components"]["docker"] = {"error": str(e)}
    
    def audit_files(self):
        """Audit de la structure des fichiers"""
        print("📁 Audit Structure...")
        
        project_dir = "/mnt/c/Users/fvegi/dev/pgi-ia"
        
        # Compter les fichiers par type
        file_stats = {
            "python": 0,
            "javascript": 0,
            "html": 0,
            "css": 0,
            "yaml": 0,
            "json": 0,
            "total": 0
        }
        
        try:
            for root, dirs, files in os.walk(project_dir):
                # Ignorer node_modules et venv
                if 'node_modules' in root or 'venv' in root:
                    continue
                    
                for file in files:
                    file_stats["total"] += 1
                    
                    if file.endswith('.py'):
                        file_stats["python"] += 1
                    elif file.endswith('.js'):
                        file_stats["javascript"] += 1
                    elif file.endswith('.html'):
                        file_stats["html"] += 1
                    elif file.endswith('.css'):
                        file_stats["css"] += 1
                    elif file.endswith('.yaml') or file.endswith('.yml'):
                        file_stats["yaml"] += 1
                    elif file.endswith('.json'):
                        file_stats["json"] += 1
            
            self.results["components"]["files"] = file_stats
            
        except Exception as e:
            self.results["components"]["files"] = {"error": str(e)}
    
    def audit_security(self):
        """Audit de sécurité basique"""
        print("🔒 Audit Sécurité...")
        
        security_checks = {
            "env_files_protected": True,
            "api_keys_exposed": False,
            "cors_configured": False,
            "https_enabled": False
        }
        
        # Vérifier les fichiers .env
        env_files = [
            "/mnt/c/Users/fvegi/dev/pgi-ia/.env",
            "/mnt/c/Users/fvegi/dev/pgi-ia/backend/.env"
        ]
        
        exposed_keys = []
        for env_file in env_files:
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    content = f.read()
                    # Vérifier si des clés sont exposées
                    if 'sk-' in content and not content.startswith('#'):
                        keys = re.findall(r'(sk-[a-zA-Z0-9]+)', content)
                        exposed_keys.extend(keys[:3])  # Limiter pour la sécurité
        
        if exposed_keys:
            security_checks["api_keys_exposed"] = True
            security_checks["exposed_count"] = len(exposed_keys)
        
        # Vérifier CORS dans le backend
        try:
            with open("/mnt/c/Users/fvegi/dev/pgi-ia/backend/main.py", 'r') as f:
                if 'CORS(app)' in f.read():
                    security_checks["cors_configured"] = True
        except:
            pass
        
        self.results["security"] = security_checks
    
    def generate_final_report(self):
        """Génère le rapport final"""
        report = []
        report.append("# 🔬 AUDIT TECHNIQUE COMPLET - PGI-IA v4.1")
        report.append(f"\n**Date**: {self.results['timestamp']}")
        
        # Backend
        report.append("\n## 🚀 Backend Status")
        if "backend" in self.results["components"]:
            for endpoint in self.results["components"]["backend"]:
                if isinstance(endpoint, dict) and "endpoint" in endpoint:
                    status = "✅" if endpoint["ok"] else "❌"
                    report.append(f"- {status} {endpoint['endpoint']}: {endpoint['status']}")
        
        # Docker
        report.append("\n## 🐳 Docker Status")
        if "docker" in self.results["components"]:
            docker = self.results["components"]["docker"]
            if "active" in docker:
                report.append(f"- **Conteneurs actifs**: {docker['active']}")
                for container in docker.get("containers", []):
                    report.append(f"  - {container['name']} ({container['image']})")
        
        # Files
        report.append("\n## 📁 Structure du Projet")
        if "files" in self.results["components"]:
            files = self.results["components"]["files"]
            report.append(f"- **Total fichiers**: {files.get('total', 0)}")
            report.append(f"- **Python**: {files.get('python', 0)} fichiers")
            report.append(f"- **JavaScript**: {files.get('javascript', 0)} fichiers")
            report.append(f"- **HTML**: {files.get('html', 0)} fichiers")
        
        # Security
        report.append("\n## 🔒 Sécurité")
        if "security" in self.results:
            sec = self.results["security"]
            report.append(f"- CORS configuré: {'✅' if sec.get('cors_configured') else '❌'}")
            report.append(f"- Clés API exposées: {'⚠️ OUI' if sec.get('api_keys_exposed') else '✅ NON'}")
            if sec.get('api_keys_exposed'):
                report.append(f"  - Nombre de clés trouvées: {sec.get('exposed_count', 0)}")
        
        return "\n".join(report)

# Exécution
if __name__ == "__main__":
    auditor = TechnicalAuditor()
    
    auditor.audit_backend()
    auditor.audit_docker()
    auditor.audit_files()
    auditor.audit_security()
    
    report = auditor.generate_final_report()
    
    # Sauvegarde
    with open("/mnt/c/Users/fvegi/dev/pgi-ia/AUDIT_TECHNIQUE.md", "w") as f:
        f.write(report)
    
    with open("/mnt/c/Users/fvegi/dev/pgi-ia/audit_technique_results.json", "w") as f:
        json.dump(auditor.results, f, indent=2)
    
    print("✅ Audit technique terminé!")
