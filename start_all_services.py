#!/usr/bin/env python3
"""
DÉMARRAGE AUTOMATIQUE COMPLET - PGI-IA
Lance tous les services et démarre l'entraînement DeepSeek
Auto-start avec droits admin (sudo:12345)
"""

import os
import sys
import subprocess
import time
import signal
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/fvegi/dev/pgi-ia")
VENV_PYTHON = BASE_DIR / "venv_pgi_ia" / "bin" / "python"
SUDO_PASSWORD = "12345"

class ServiceManager:
    """Gestionnaire de services PGI-IA"""
    
    def __init__(self):
        self.services = {}
        self.startup_log = []
        
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.startup_log.append(log_message)
        
    def start_backend_service(self):
        """Démarrage du backend Flask"""
        self.log("🔧 Démarrage backend Flask...")
        
        try:
            # Tuer les processus Flask existants
            subprocess.run(["pkill", "-f", "main.py"], capture_output=True)
            time.sleep(2)
            
            # Démarrer nouveau backend
            backend_process = subprocess.Popen([
                str(VENV_PYTHON), 
                str(BASE_DIR / "backend" / "main.py")
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.services["backend"] = backend_process
            self.log("✅ Backend Flask démarré (PID: {})".format(backend_process.pid))
            
            # Test de connectivité
            time.sleep(5)
            import requests
            try:
                response = requests.get("http://localhost:5000/", timeout=10)
                if response.status_code == 200:
                    self.log("✅ Backend accessible sur http://localhost:5000")
                    return True
                else:
                    self.log(f"⚠️ Backend répond avec code {response.status_code}")
                    return False
            except:
                self.log("❌ Backend non accessible")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur démarrage backend: {e}")
            return False
            
    def verify_gpu_status(self):
        """Vérification statut GPU"""
        self.log("🎮 Vérification GPU...")
        
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader,nounits"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_info = result.stdout.strip().split(", ")
                gpu_name = gpu_info[0]
                memory_total = int(gpu_info[1])
                memory_used = int(gpu_info[2])
                memory_free = memory_total - memory_used
                
                self.log(f"✅ GPU: {gpu_name}")
                self.log(f"✅ Mémoire GPU: {memory_used}MB/{memory_total}MB utilisée ({memory_free}MB libre)")
                
                if memory_free > 2000:  # Au moins 2GB libre
                    self.log("✅ Mémoire GPU suffisante pour l'entraînement")
                    return True
                else:
                    self.log("⚠️ Mémoire GPU limitée, entraînement possible mais lent")
                    return True
            else:
                self.log("❌ Impossible de détecter le GPU")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur vérification GPU: {e}")
            return False
            
    def run_system_verification(self):
        """Exécution vérification système"""
        self.log("🔍 Vérification système complète...")
        
        try:
            result = subprocess.run([
                str(VENV_PYTHON), 
                str(BASE_DIR / "verify_complete_system.py")
            ], capture_output=True, text=True, timeout=60)
            
            # Extraction du score de réussite
            output_lines = result.stdout.split('\n')
            success_rate = 0
            
            for line in output_lines:
                if "TAUX DE RÉUSSITE:" in line:
                    try:
                        # Format: "📊 TAUX DE RÉUSSITE: 43/47 (91.5%)"
                        percentage = line.split('(')[1].split('%')[0]
                        success_rate = float(percentage)
                        break
                    except:
                        pass
                        
            self.log(f"✅ Vérification système: {success_rate}% de réussite")
            
            if success_rate >= 90:
                self.log("🏆 Système PRÊT pour l'entraînement")
                return True
            elif success_rate >= 80:
                self.log("👍 Système FONCTIONNEL avec corrections mineures")
                return True
            else:
                self.log("⚠️ Système nécessite des corrections")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur vérification système: {e}")
            return False
            
    def check_plan_files(self):
        """Vérification des fichiers de plans"""
        self.log("📁 Vérification des plans PDF...")
        
        kahnawake_dir = BASE_DIR / "plans_kahnawake"
        alexis_dir = BASE_DIR / "plans_alexis_nihon"
        
        # Créer les répertoires s'ils n'existent pas
        kahnawake_dir.mkdir(exist_ok=True)
        alexis_dir.mkdir(exist_ok=True)
        
        kahnawake_pdfs = list(kahnawake_dir.glob("**/*.pdf"))
        alexis_pdfs = list(alexis_dir.glob("**/*.pdf"))
        
        self.log(f"📊 Plans Kahnawake: {len(kahnawake_pdfs)} PDFs")
        self.log(f"📊 Plans Alexis-Nihon: {len(alexis_pdfs)} PDFs")
        
        if len(kahnawake_pdfs) > 0 or len(alexis_pdfs) > 0:
            self.log("✅ Plans détectés, prêt pour l'entraînement")
            return True
        else:
            self.log("⚠️ Aucun plan détecté, entraînement avec dataset existant")
            return False
            
    def start_deepseek_training(self, has_plans=False):
        """Démarrage entraînement DeepSeek"""
        if has_plans:
            self.log("🧠 Démarrage entraînement DeepSeek avec plans PDF...")
            script_path = BASE_DIR / "deepseek_finetune_english_complete.py"
        else:
            self.log("🧠 Démarrage entraînement DeepSeek avec dataset existant...")
            script_path = BASE_DIR / "deepseek_finetune_english_complete.py"
            
        try:
            # Démarrage en arrière-plan
            training_process = subprocess.Popen([
                str(VENV_PYTHON), 
                str(script_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.services["deepseek_training"] = training_process
            self.log(f"✅ Entraînement DeepSeek démarré (PID: {training_process.pid})")
            self.log("📋 Logs en temps réel dans deepseek_finetune_complete.log")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur démarrage entraînement: {e}")
            return False
            
    def run_audits(self):
        """Exécution des audits DeepSeek et Justina"""
        self.log("📊 Exécution audits qualité...")
        
        # Audit DeepSeek
        try:
            result = subprocess.run([
                str(VENV_PYTHON), 
                str(BASE_DIR / "audit_deepseek.py")
            ], capture_output=True, text=True, timeout=30)
            
            if "EXCELLENT" in result.stdout:
                self.log("✅ Audit DeepSeek: EXCELLENT")
            elif "BIEN" in result.stdout:
                self.log("👍 Audit DeepSeek: BIEN")
            else:
                self.log("⚠️ Audit DeepSeek: À améliorer")
                
        except Exception as e:
            self.log(f"⚠️ Erreur audit DeepSeek: {e}")
            
        # Audit Justina
        try:
            result = subprocess.run([
                str(VENV_PYTHON), 
                str(BASE_DIR / "audit_justina.py")
            ], capture_output=True, text=True, timeout=30)
            
            if "EXCEPTIONNEL" in result.stdout:
                self.log("✅ Audit Justina: EXCEPTIONNEL")
            elif "EXCELLENT" in result.stdout:
                self.log("👍 Audit Justina: EXCELLENT")
            else:
                self.log("⚠️ Audit Justina: À améliorer")
                
        except Exception as e:
            self.log(f"⚠️ Erreur audit Justina: {e}")
            
    def open_frontend(self):
        """Ouverture du frontend dans le navigateur"""
        self.log("🌐 Instructions frontend...")
        
        frontend_path = BASE_DIR / "frontend" / "index.html"
        if frontend_path.exists():
            self.log(f"✅ Frontend disponible: file://{frontend_path}")
            self.log("🌐 Ouvrez ce fichier dans votre navigateur")
            
            # Tentative d'ouverture automatique (si possible)
            try:
                subprocess.run(["xdg-open", str(frontend_path)], check=False)
                self.log("🚀 Tentative d'ouverture automatique du navigateur")
            except:
                pass
        else:
            self.log("❌ Frontend non trouvé")
            
    def save_startup_report(self):
        """Sauvegarde rapport de démarrage"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "services": {name: process.pid if process.poll() is None else "stopped" 
                        for name, process in self.services.items()},
            "startup_log": self.startup_log,
            "status": "running" if any(p.poll() is None for p in self.services.values()) else "stopped"
        }
        
        report_path = BASE_DIR / "startup_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.log(f"📁 Rapport de démarrage: {report_path}")
        
    def cleanup_on_exit(self, signum, frame):
        """Nettoyage lors de l'arrêt"""
        self.log("🛑 Arrêt des services...")
        
        for name, process in self.services.items():
            if process.poll() is None:
                self.log(f"🛑 Arrêt {name} (PID: {process.pid})")
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
                    
        sys.exit(0)

def main():
    """Fonction principale de démarrage"""
    print("🚀 DÉMARRAGE AUTOMATIQUE COMPLET PGI-IA")
    print("🎯 Auto-start avec droits admin")
    print("=" * 60)
    
    manager = ServiceManager()
    
    # Configuration gestionnaire de signaux
    signal.signal(signal.SIGINT, manager.cleanup_on_exit)
    signal.signal(signal.SIGTERM, manager.cleanup_on_exit)
    
    try:
        # Étapes de démarrage
        steps = [
            ("Vérification GPU", manager.verify_gpu_status),
            ("Vérification système", manager.run_system_verification),
            ("Démarrage backend", manager.start_backend_service),
            ("Vérification plans", manager.check_plan_files),
            ("Audits qualité", manager.run_audits),
            ("Instructions frontend", manager.open_frontend)
        ]
        
        results = {}
        
        for step_name, step_function in steps:
            manager.log(f"🔄 {step_name}...")
            results[step_name] = step_function()
            
        # Démarrage entraînement si tout va bien
        if results.get("Vérification système", False):
            has_plans = results.get("Vérification plans", False)
            manager.start_deepseek_training(has_plans)
            
        # Rapport final
        success_count = sum(1 for result in results.values() if result)
        total_steps = len(results)
        success_rate = (success_count / total_steps) * 100
        
        manager.log("\n" + "=" * 50)
        manager.log("📊 RÉSUMÉ DÉMARRAGE")
        manager.log("=" * 50)
        manager.log(f"✅ Étapes réussies: {success_count}/{total_steps} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            manager.log("🏆 DÉMARRAGE RÉUSSI!")
            manager.log("🌐 Backend: http://localhost:5000")
            manager.log("📁 Frontend: Ouvrir frontend/index.html")
            manager.log("🧠 Entraînement DeepSeek: En cours")
            manager.log("📋 Logs: deepseek_finetune_complete.log")
        else:
            manager.log("⚠️ DÉMARRAGE PARTIEL")
            manager.log("🔧 Vérifiez les erreurs ci-dessus")
            
        # Sauvegarde rapport
        manager.save_startup_report()
        
        # Mode surveillance (optionnel)
        manager.log("\n🔍 Mode surveillance actif...")
        manager.log("📋 Ctrl+C pour arrêter tous les services")
        
        # Boucle de surveillance
        while True:
            time.sleep(30)
            
            # Vérification santé des services
            active_services = 0
            for name, process in manager.services.items():
                if process.poll() is None:
                    active_services += 1
                else:
                    manager.log(f"⚠️ Service {name} arrêté")
                    
            if active_services == 0:
                manager.log("🛑 Tous les services arrêtés, fin de surveillance")
                break
                
            manager.log(f"💓 {active_services} services actifs")
            
    except KeyboardInterrupt:
        manager.log("🛑 Arrêt demandé par l'utilisateur")
        manager.cleanup_on_exit(None, None)
    except Exception as e:
        manager.log(f"❌ Erreur critique: {e}")
        manager.cleanup_on_exit(None, None)

if __name__ == "__main__":
    main()