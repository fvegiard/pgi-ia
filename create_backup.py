#!/usr/bin/env python3
"""
CRÉATION BACKUP COMPLET PGI-IA
Sauvegarde complète du projet avec tous les fichiers importants
"""

import os
import shutil
import tarfile
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/fvegi/dev/pgi-ia")
BACKUP_DIR = Path("/home/fvegi/dev/backups")

class BackupManager:
    """Gestionnaire de backup complet PGI-IA"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_name = f"pgi-ia_backup_{self.timestamp}"
        self.backup_path = BACKUP_DIR / self.backup_name
        self.files_backed_up = []
        self.total_size = 0
        
    def create_backup_structure(self):
        """Création structure de backup"""
        print("🔧 CRÉATION BACKUP COMPLET PGI-IA")
        print("=" * 50)
        
        # Créer répertoire backup
        BACKUP_DIR.mkdir(exist_ok=True)
        self.backup_path.mkdir(exist_ok=True)
        
        print(f"📁 Répertoire backup: {self.backup_path}")
        
    def backup_source_code(self):
        """Backup du code source"""
        print("\n📦 Backup code source...")
        
        # Fichiers Python critiques
        python_files = [
            "backend/main.py",
            "backend/agents/orchestrator.py",
            "backend/agents/directive_agent.py",
            "frontend/index.html",
            "frontend/script.js",
            "frontend/style.css",
            "audit_deepseek.py",
            "audit_justina.py",
            "train_deepseek_kahnawake_plans.py",
            "deepseek_finetune_english_complete.py",
            "verify_complete_system.py",
            "setup_complete_environment.py",
            "start_all_services.py",
            "create_backup.py"
        ]
        
        for file_path in python_files:
            src = BASE_DIR / file_path
            if src.exists():
                # Créer structure de répertoires
                dest_dir = self.backup_path / Path(file_path).parent
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                # Copier fichier
                dest = self.backup_path / file_path
                shutil.copy2(src, dest)
                
                file_size = src.stat().st_size
                self.files_backed_up.append(str(file_path))
                self.total_size += file_size
                
                print(f"✅ {file_path} ({file_size:,} bytes)")
                
    def backup_configuration(self):
        """Backup configuration et documentation"""
        print("\n📋 Backup configuration...")
        
        config_files = [
            "config/agents.yaml",
            "config/agents.example.yaml",
            "README.md",
            "CLAUDE.md",
            "MISSION_ACCOMPLIE.md",
            "requirements.txt",
            "requirements_complete.txt",
            "backend/requirements.txt",
            ".gitignore",
            "activate_pgi_ia.sh",
            "start_pgi_ia.py"
        ]
        
        for file_path in config_files:
            src = BASE_DIR / file_path
            if src.exists():
                dest_dir = self.backup_path / Path(file_path).parent
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                dest = self.backup_path / file_path
                shutil.copy2(src, dest)
                
                file_size = src.stat().st_size
                self.files_backed_up.append(str(file_path))
                self.total_size += file_size
                
                print(f"✅ {file_path}")
                
    def backup_datasets(self):
        """Backup datasets et modèles"""
        print("\n📊 Backup datasets...")
        
        dataset_files = [
            "deepseek_training_dataset.jsonl",
            "system_verification_report.json",
            "startup_report.json"
        ]
        
        for file_path in dataset_files:
            src = BASE_DIR / file_path
            if src.exists():
                dest = self.backup_path / file_path
                shutil.copy2(src, dest)
                
                file_size = src.stat().st_size
                self.files_backed_up.append(str(file_path))
                self.total_size += file_size
                
                print(f"✅ {file_path} ({file_size:,} bytes)")
                
    def backup_data_samples(self):
        """Backup échantillons de données"""
        print("\n🗂️ Backup structures données...")
        
        # Créer structure vide pour les plans
        (self.backup_path / "plans_kahnawake" / ".placeholder").parent.mkdir(parents=True, exist_ok=True)
        (self.backup_path / "plans_kahnawake" / ".placeholder").touch()
        
        (self.backup_path / "plans_alexis_nihon" / ".placeholder").parent.mkdir(parents=True, exist_ok=True)
        (self.backup_path / "plans_alexis_nihon" / ".placeholder").touch()
        
        # Structure data
        (self.backup_path / "data" / "drop_zone" / ".placeholder").parent.mkdir(parents=True, exist_ok=True)
        (self.backup_path / "data" / "drop_zone" / ".placeholder").touch()
        
        print("✅ Structure répertoires créée")
        
    def create_environment_snapshot(self):
        """Snapshot de l'environnement"""
        print("\n🔧 Snapshot environnement...")
        
        env_info = {
            "timestamp": datetime.now().isoformat(),
            "python_version": os.popen("python3 --version").read().strip(),
            "system": dict(zip(['sysname', 'nodename', 'release', 'version', 'machine'], os.uname())) if hasattr(os, 'uname') else {},
            "environment_variables": {
                "OPENAI_API_KEY": "***" if os.getenv("OPENAI_API_KEY") else "Not set",
                "DEEPSEEK_API_KEY": "***" if os.getenv("DEEPSEEK_API_KEY") else "Not set",
                "ANTHROPIC_API_KEY": "***" if os.getenv("ANTHROPIC_API_KEY") else "Not set",
                "GOOGLE_API_KEY": "***" if os.getenv("GOOGLE_API_KEY") else "Not set"
            },
            "gpu_status": os.popen("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null").read().strip(),
            "venv_path": str(BASE_DIR / "venv_pgi_ia"),
            "files_backed_up": len(self.files_backed_up),
            "total_size_bytes": self.total_size
        }
        
        # Sauvegarder packages installés
        if (BASE_DIR / "venv_pgi_ia" / "bin" / "pip").exists():
            packages = os.popen(f"{BASE_DIR}/venv_pgi_ia/bin/pip freeze").read()
            with open(self.backup_path / "pip_freeze.txt", 'w') as f:
                f.write(packages)
            print("✅ Liste packages pip sauvegardée")
            
        # Sauvegarder info environnement
        with open(self.backup_path / "environment_snapshot.json", 'w') as f:
            json.dump(env_info, f, indent=2)
            
        print("✅ Snapshot environnement créé")
        
    def create_restore_script(self):
        """Créer script de restauration"""
        print("\n📜 Création script restauration...")
        
        restore_script = f"""#!/bin/bash
# Script de restauration backup PGI-IA
# Créé le: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

echo "🔧 RESTAURATION BACKUP PGI-IA"
echo "============================"

# Vérifier répertoire destination
if [ -z "$1" ]; then
    echo "Usage: ./restore_backup.sh /chemin/destination"
    exit 1
fi

DEST_DIR="$1"
BACKUP_DIR="$(dirname "$0")"

echo "📁 Source: $BACKUP_DIR"
echo "📁 Destination: $DEST_DIR"
echo ""

# Confirmation
read -p "Confirmer restauration? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Restauration annulée"
    exit 1
fi

# Créer destination
mkdir -p "$DEST_DIR"

# Copier fichiers
echo "📦 Copie des fichiers..."
cp -r "$BACKUP_DIR"/* "$DEST_DIR/"

# Recréer environnement virtuel
echo "🐍 Recréation environnement virtuel..."
cd "$DEST_DIR"
python3 -m venv venv_pgi_ia

# Installer dépendances
echo "📦 Installation dépendances..."
./venv_pgi_ia/bin/pip install --upgrade pip
./venv_pgi_ia/bin/pip install -r requirements_complete.txt

# Permissions
chmod +x activate_pgi_ia.sh
chmod +x start_all_services.py

echo ""
echo "✅ RESTAURATION TERMINÉE!"
echo ""
echo "🚀 Pour démarrer:"
echo "   source $DEST_DIR/activate_pgi_ia.sh"
echo "   python start_all_services.py"
"""
        
        restore_path = self.backup_path / "restore_backup.sh"
        with open(restore_path, 'w') as f:
            f.write(restore_script)
            
        os.chmod(restore_path, 0o755)
        print("✅ Script restauration créé")
        
    def create_archive(self):
        """Créer archive tar.gz"""
        print("\n📦 Création archive compressée...")
        
        archive_name = f"{self.backup_name}.tar.gz"
        archive_path = BACKUP_DIR / archive_name
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.backup_path, arcname=self.backup_name)
            
        archive_size = archive_path.stat().st_size
        
        print(f"✅ Archive créée: {archive_path}")
        print(f"📏 Taille: {archive_size / 1024 / 1024:.2f} MB")
        
        return archive_path
        
    def create_backup_report(self):
        """Créer rapport de backup"""
        report = {
            "backup_name": self.backup_name,
            "timestamp": datetime.now().isoformat(),
            "files_count": len(self.files_backed_up),
            "total_size_bytes": self.total_size,
            "total_size_mb": self.total_size / 1024 / 1024,
            "files_list": sorted(self.files_backed_up),
            "backup_location": str(self.backup_path),
            "archive_location": str(BACKUP_DIR / f"{self.backup_name}.tar.gz")
        }
        
        report_path = self.backup_path / "backup_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📋 Rapport backup: {report_path}")
        
        return report

def main():
    """Fonction principale backup"""
    manager = BackupManager()
    
    try:
        # Étapes backup
        manager.create_backup_structure()
        manager.backup_source_code()
        manager.backup_configuration()
        manager.backup_datasets()
        manager.backup_data_samples()
        manager.create_environment_snapshot()
        manager.create_restore_script()
        
        # Créer archive
        archive_path = manager.create_archive()
        
        # Rapport final
        report = manager.create_backup_report()
        
        print("\n" + "=" * 50)
        print("✅ BACKUP COMPLET RÉUSSI!")
        print("=" * 50)
        print(f"📁 Backup: {manager.backup_path}")
        print(f"📦 Archive: {archive_path}")
        print(f"📊 Fichiers: {report['files_count']}")
        print(f"💾 Taille: {report['total_size_mb']:.2f} MB")
        print("\n🔧 Pour restaurer:")
        print(f"   tar -xzf {archive_path}")
        print(f"   cd {manager.backup_name}")
        print("   ./restore_backup.sh /nouveau/chemin")
        
    except Exception as e:
        print(f"\n❌ Erreur backup: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)