#!/usr/bin/env python3
"""
Audit Expert IA avec DeepSeek - 5 tours de communication
Analyse approfondie du système PGI-IA par un expert IA codeur
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI

# Configuration DeepSeek
DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

class DeepSeekAuditor:
    def __init__(self):
        self.conversation_history = []
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "rounds": [],
            "final_report": None,
            "recommendations": []
        }
        
    def analyze_system_state(self):
        """Collecte l'état actuel du système"""
        system_info = {
            "files_structure": self._get_file_structure(),
            "uncommitted_changes": self._get_git_status(),
            "dependencies_status": self._check_dependencies(),
            "docker_status": self._check_docker_setup(),
            "recent_work": self._get_recent_modifications()
        }
        return system_info
    
    def _get_file_structure(self):
        """Analyse la structure des fichiers"""
        structure = {}
        for root, dirs, files in os.walk('/home/fvegi/dev/pgi-ia'):
            # Skip venv and cache
            dirs[:] = [d for d in dirs if d not in ['venv_pgi_ia', '__pycache__', '.git', 'node_modules']]
            
            rel_path = os.path.relpath(root, '/home/fvegi/dev/pgi-ia')
            if rel_path == '.':
                rel_path = 'root'
            
            structure[rel_path] = {
                'dirs': dirs,
                'files': files[:20]  # Limit files per directory
            }
        return structure
    
    def _get_git_status(self):
        """Récupère le statut git"""
        import subprocess
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd='/home/fvegi/dev/pgi-ia')
            return result.stdout.strip().split('\n') if result.stdout else []
        except:
            return ["Error getting git status"]
    
    def _check_dependencies(self):
        """Vérifie les dépendances Python"""
        missing = []
        critical_packages = ['flask', 'flask-cors', 'pyyaml', 'openai', 'torch']
        
        import subprocess
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        installed_packages = result.stdout.lower()
        
        for package in critical_packages:
            if package not in installed_packages:
                missing.append(package)
        
        return {
            "missing_critical": missing,
            "total_packages": len(installed_packages.split('\n'))
        }
    
    def _check_docker_setup(self):
        """Vérifie la configuration Docker"""
        docker_files = {
            "docker-compose.yml": os.path.exists('/home/fvegi/dev/pgi-ia/docker-compose.yml'),
            "docker-compose.dev.yml": os.path.exists('/home/fvegi/dev/pgi-ia/docker-compose.dev.yml'),
            "Dockerfile": os.path.exists('/home/fvegi/dev/pgi-ia/Dockerfile'),
            "docker_deploy.sh": os.path.exists('/home/fvegi/dev/pgi-ia/docker-deploy.sh'),
            ".dockerignore": os.path.exists('/home/fvegi/dev/pgi-ia/.dockerignore')
        }
        return docker_files
    
    def _get_recent_modifications(self):
        """Récupère les modifications récentes"""
        import subprocess
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                                  capture_output=True, text=True, cwd='/home/fvegi/dev/pgi-ia')
            return result.stdout.strip().split('\n') if result.stdout else []
        except:
            return ["Error getting git log"]
    
    def communicate_with_deepseek(self, round_num, system_info, previous_analysis=None):
        """Communique avec DeepSeek pour l'audit"""
        
        if round_num == 1:
            prompt = f"""
            Tu es un expert IA senior spécialisé en architecture logicielle et développement Python/Flask.
            
            Je suis Claude Code et j'ai besoin de ton expertise pour auditer le projet PGI-IA.
            
            Contexte: J'ai développé un système de gestion électrique industrielle avec IA, mais l'utilisateur
            a identifié des problèmes de référencement de fichiers et des manquements dans mon travail.
            
            Voici l'état actuel du système:
            {json.dumps(system_info, indent=2)}
            
            Analyse critique:
            1. Quels sont les problèmes architecturaux majeurs?
            2. Quels fichiers semblent mal organisés ou non référencés?
            3. Quelles sont les failles dans l'implémentation?
            4. Qu'est-ce qui manque pour un système production-ready?
            
            Sois direct et critique - j'ai besoin d'identifier mes erreurs.
            """
        
        elif round_num == 2:
            prompt = f"""
            Merci pour ton analyse initiale. Maintenant, concentrons-nous sur les solutions.
            
            Basé sur ton analyse précédente:
            {previous_analysis}
            
            Questions spécifiques:
            1. Comment réorganiser proprement les fichiers Python du root?
            2. Quelle architecture Docker recommandes-tu pour ce projet multi-services?
            3. Comment corriger les problèmes de dépendances sans casser le système?
            4. Quels tests automatisés sont critiques à implémenter?
            
            Propose des solutions concrètes et réalisables.
            """
            
        elif round_num == 3:
            prompt = f"""
            Excellentes propositions. Maintenant, aidons-moi à prioriser.
            
            Considérant:
            - L'utilisateur veut un système fonctionnel rapidement
            - Le dashboard avec plan zoomable vient d'être ajouté
            - Docker doit être opérationnel
            - 11 fichiers non committés attendent
            
            Questions:
            1. Dans quel ordre exact dois-je procéder?
            2. Quels sont les risques de chaque étape?
            3. Comment éviter de casser ce qui fonctionne déjà?
            4. Quelle stratégie de commit/push adopter?
            
            J'ai besoin d'un plan d'action séquencé et sûr.
            """
            
        elif round_num == 4:
            prompt = f"""
            Analysons maintenant les aspects IA et performance du système.
            
            Le système doit:
            - Traiter 300+ PDFs de plans électriques
            - Utiliser GPU RTX 4060 (8GB)
            - Intégrer DeepSeek, Gemini (à configurer)
            - Extraire texte, analyser, classifier
            
            Questions critiques:
            1. L'architecture actuelle peut-elle gérer cette charge?
            2. Comment optimiser l'utilisation GPU avec Docker?
            3. Quels goulots d'étranglement vois-tu?
            4. Recommandations pour le pipeline de traitement PDF?
            
            Focus sur scalabilité et performance.
            """
            
        else:  # round 5
            prompt = f"""
            Dernière analyse - Vue d'ensemble et recommandations finales.
            
            Après nos 4 tours d'analyse, aide-moi à créer:
            
            1. Un rapport exécutif des problèmes critiques
            2. Une roadmap de correction priorisée
            3. Les métriques de succès à surveiller
            4. Les pièges à éviter absolument
            
            Synthétise tout en gardant en tête que l'utilisateur attend:
            - Un système Docker fonctionnel
            - Une organisation claire des fichiers
            - Une architecture scalable pour l'IA
            - Une documentation des décisions prises
            
            Sois concis mais exhaustif.
            """
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Tu es un expert IA senior avec 15 ans d'expérience en architecture logicielle."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur DeepSeek: {str(e)}"
    
    def run_audit(self):
        """Exécute l'audit complet en 5 tours"""
        print("🔍 Démarrage de l'audit expert avec DeepSeek...")
        
        # Analyse initiale du système
        system_info = self.analyze_system_state()
        
        previous_analysis = None
        
        for round_num in range(1, 6):
            print(f"\n📊 Tour {round_num}/5 - Communication avec DeepSeek...")
            
            analysis = self.communicate_with_deepseek(round_num, system_info, previous_analysis)
            
            self.audit_results["rounds"].append({
                "round": round_num,
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis
            })
            
            previous_analysis = analysis
            
            # Petit délai entre les requêtes
            time.sleep(2)
        
        # Génération du rapport final
        self.generate_final_report()
        
        return self.audit_results
    
    def generate_final_report(self):
        """Génère le rapport final consolidé"""
        report = {
            "executive_summary": "Audit complet du système PGI-IA",
            "critical_issues": [],
            "recommendations": [],
            "action_plan": [],
            "success_metrics": []
        }
        
        # Extraction des points clés de chaque tour
        for round_data in self.audit_results["rounds"]:
            if "critique" in round_data["analysis"].lower():
                report["critical_issues"].append(round_data["analysis"][:200] + "...")
        
        self.audit_results["final_report"] = report
    
    def save_report(self):
        """Sauvegarde le rapport d'audit"""
        filename = f"audit_deepseek_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/home/fvegi/dev/pgi-ia/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Rapport d'audit sauvegardé: {filename}")
        return filepath

if __name__ == "__main__":
    auditor = DeepSeekAuditor()
    results = auditor.run_audit()
    report_path = auditor.save_report()
    
    print("\n🎯 Audit terminé!")
    print(f"📄 Rapport disponible: {report_path}")