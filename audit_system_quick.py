#!/usr/bin/env python3
"""
Audit rapide du système PGI-IA
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class SystemAuditor:
    def __init__(self):
        self.project_root = Path("/home/fvegi/dev/pgi-ia")
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "recommendations": [],
            "file_analysis": {},
            "dependency_status": {},
            "docker_status": {}
        }
    
    def analyze_file_structure(self):
        """Analyse la structure des fichiers et identifie les problèmes"""
        print("📁 Analyse de la structure des fichiers...")
        
        # Fichiers Python dans le root (mauvaise pratique)
        root_py_files = list(self.project_root.glob("*.py"))
        if len(root_py_files) > 10:
            self.audit_results["issues"].append({
                "severity": "HIGH",
                "type": "file_organization",
                "description": f"{len(root_py_files)} fichiers Python dans le root - devrait être dans scripts/",
                "files": [f.name for f in root_py_files[:10]] + ["..."]
            })
        
        # Fichiers non committés
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            uncommitted = result.stdout.strip().split('\n') if result.stdout else []
            if len(uncommitted) > 5:
                self.audit_results["issues"].append({
                    "severity": "MEDIUM",
                    "type": "version_control",
                    "description": f"{len(uncommitted)} fichiers non committés",
                    "files": uncommitted
                })
        except:
            pass
        
        # Vérifier les dossiers critiques
        critical_dirs = ['backend', 'frontend', 'config', 'docker', 'tests']
        for dir_name in critical_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                self.audit_results["issues"].append({
                    "severity": "HIGH",
                    "type": "missing_directory",
                    "description": f"Dossier critique manquant: {dir_name}"
                })
        
        # Analyser les fichiers de log
        log_files = list(self.project_root.glob("*.log"))
        if log_files:
            self.audit_results["issues"].append({
                "severity": "LOW",
                "type": "file_organization",
                "description": f"{len(log_files)} fichiers log dans le root - devrait être dans logs/",
                "files": [f.name for f in log_files]
            })
        
        return self.audit_results
    
    def check_dependencies(self):
        """Vérifie les dépendances critiques"""
        print("📦 Vérification des dépendances...")
        
        critical_packages = {
            'flask': 'Backend web framework',
            'flask-cors': 'CORS support',
            'pyyaml': 'Configuration files',
            'openai': 'AI API client',
            'torch': 'Deep learning',
            'transformers': 'NLP models',
            'pdf2image': 'PDF processing',
            'pytesseract': 'OCR'
        }
        
        # Liste des packages installés
        result = subprocess.run([str(self.project_root / 'venv_pgi_ia/bin/pip'), 'list', '--format=json'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            installed = {pkg['name'].lower(): pkg['version'] 
                        for pkg in json.loads(result.stdout)}
            
            for package, description in critical_packages.items():
                if package not in installed:
                    self.audit_results["issues"].append({
                        "severity": "CRITICAL",
                        "type": "missing_dependency",
                        "description": f"Package manquant: {package} - {description}"
                    })
                    self.audit_results["dependency_status"][package] = "MISSING"
                else:
                    self.audit_results["dependency_status"][package] = installed[package]
    
    def check_docker_setup(self):
        """Vérifie la configuration Docker"""
        print("🐳 Vérification Docker...")
        
        docker_files = {
            'docker-compose.yml': 'Main compose file',
            'docker-compose.dev.yml': 'Dev compose file',
            'Dockerfile': 'Main Dockerfile',
            '.dockerignore': 'Docker ignore file',
            'docker/backend.Dockerfile': 'Backend Dockerfile'
        }
        
        for file_path, description in docker_files.items():
            full_path = self.project_root / file_path
            exists = full_path.exists()
            self.audit_results["docker_status"][file_path] = exists
            
            if not exists and 'Dockerfile' in file_path:
                self.audit_results["issues"].append({
                    "severity": "HIGH",
                    "type": "docker_config",
                    "description": f"Fichier Docker manquant: {file_path} - {description}"
                })
    
    def generate_recommendations(self):
        """Génère les recommandations basées sur l'analyse"""
        print("💡 Génération des recommandations...")
        
        # Priorité 1: Dépendances critiques
        missing_deps = [issue for issue in self.audit_results["issues"] 
                       if issue["type"] == "missing_dependency"]
        if missing_deps:
            self.audit_results["recommendations"].append({
                "priority": 1,
                "action": "Installer les dépendances manquantes",
                "command": f"cd {self.project_root} && ./venv_pgi_ia/bin/pip install flask flask-cors pyyaml",
                "impact": "CRITIQUE - Le système ne peut pas démarrer sans ces packages"
            })
        
        # Priorité 2: Fichiers non committés
        uncommitted = [issue for issue in self.audit_results["issues"] 
                      if issue["type"] == "version_control"]
        if uncommitted:
            self.audit_results["recommendations"].append({
                "priority": 2,
                "action": "Committer ou stash les changements",
                "command": "git add . && git commit -m 'feat: Plan integration with zoom/pan'",
                "impact": "IMPORTANT - Risque de perte de travail"
            })
        
        # Priorité 3: Organisation des fichiers
        file_org_issues = [issue for issue in self.audit_results["issues"] 
                          if issue["type"] == "file_organization"]
        if file_org_issues:
            self.audit_results["recommendations"].append({
                "priority": 3,
                "action": "Réorganiser les fichiers Python",
                "command": "mkdir -p scripts && mv *.py scripts/ (sauf main.py)",
                "impact": "MOYEN - Améliore la maintenabilité"
            })
        
        # Priorité 4: Docker
        docker_issues = [issue for issue in self.audit_results["issues"] 
                        if issue["type"] == "docker_config"]
        if docker_issues:
            self.audit_results["recommendations"].append({
                "priority": 4,
                "action": "Créer Dockerfile manquant",
                "command": "Utiliser docker/backend.Dockerfile comme base",
                "impact": "MOYEN - Nécessaire pour Docker"
            })
    
    def run_audit(self):
        """Exécute l'audit complet"""
        print("🔍 Démarrage de l'audit du système PGI-IA...")
        print("=" * 50)
        
        self.analyze_file_structure()
        self.check_dependencies()
        self.check_docker_setup()
        self.generate_recommendations()
        
        # Sauvegarder le rapport
        report_path = self.project_root / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        
        print(f"\n✅ Audit terminé! Rapport sauvé: {report_path}")
        
        # Afficher le résumé
        self.display_summary()
        
        return self.audit_results
    
    def display_summary(self):
        """Affiche un résumé de l'audit"""
        print("\n📊 RÉSUMÉ DE L'AUDIT")
        print("=" * 50)
        
        # Compter les issues par sévérité
        severity_count = {}
        for issue in self.audit_results["issues"]:
            severity = issue["severity"]
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        print(f"\n🔴 Issues trouvées:")
        for severity, count in sorted(severity_count.items()):
            print(f"  - {severity}: {count}")
        
        print(f"\n💡 Recommandations: {len(self.audit_results['recommendations'])}")
        for rec in sorted(self.audit_results["recommendations"], key=lambda x: x["priority"]):
            print(f"  {rec['priority']}. {rec['action']}")
        
        # Issues critiques
        critical = [i for i in self.audit_results["issues"] if i["severity"] == "CRITICAL"]
        if critical:
            print(f"\n⚠️  ATTENTION: {len(critical)} issues CRITIQUES détectées!")
            for issue in critical:
                print(f"  - {issue['description']}")

if __name__ == "__main__":
    auditor = SystemAuditor()
    auditor.run_audit()