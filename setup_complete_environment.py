#!/usr/bin/env python3
"""
CONFIGURATION COMPLÈTE DE L'ENVIRONNEMENT PGI-IA
Résolution des conflits NumPy et installation de toutes les dépendances
Auto-setup avec environnement virtuel propre
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path("/home/fvegi/dev/pgi-ia")
VENV_DIR = BASE_DIR / "venv_pgi_ia"

def create_clean_virtual_environment():
    """Création d'un environnement virtuel propre"""
    print("🔧 CRÉATION ENVIRONNEMENT VIRTUEL PROPRE")
    print("=" * 50)
    
    # Suppression de l'ancien environnement s'il existe
    if VENV_DIR.exists():
        print(f"🗑️ Suppression ancien environnement: {VENV_DIR}")
        shutil.rmtree(VENV_DIR)
    
    # Création du nouvel environnement
    try:
        print(f"📦 Création environnement virtuel: {VENV_DIR}")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        print("✅ Environnement virtuel créé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur création environnement: {e}")
        return False

def get_venv_python():
    """Obtenir le chemin vers Python de l'environnement virtuel"""
    if os.name == 'nt':  # Windows
        return VENV_DIR / "Scripts" / "python.exe"
    else:  # Linux/Mac
        return VENV_DIR / "bin" / "python"

def get_venv_pip():
    """Obtenir le chemin vers pip de l'environnement virtuel"""
    if os.name == 'nt':  # Windows
        return VENV_DIR / "Scripts" / "pip"
    else:  # Linux/Mac
        return VENV_DIR / "bin" / "pip"

def upgrade_pip():
    """Mise à jour de pip dans l'environnement virtuel"""
    print("\n📦 MISE À JOUR PIP")
    print("=" * 50)
    
    pip_path = get_venv_pip()
    python_path = get_venv_python()
    
    try:
        subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("✅ Pip mis à jour avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur mise à jour pip: {e}")
        return False

def install_base_dependencies():
    """Installation des dépendances de base avec versions compatibles"""
    print("\n📦 INSTALLATION DÉPENDANCES DE BASE")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    # Dépendances critiques avec versions spécifiques pour éviter les conflits
    base_packages = [
        "numpy==1.24.3",  # Version stable compatible
        "setuptools>=68.0.0",
        "wheel>=0.41.0",
        "cython>=0.29.36"
    ]
    
    for package in base_packages:
        try:
            print(f"📥 Installation: {package}")
            subprocess.run([str(python_path), "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation {package}: {e}")
            return False
    
    return True

def install_ml_dependencies():
    """Installation des dépendances ML/AI"""
    print("\n🤖 INSTALLATION DÉPENDANCES ML/AI")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    ml_packages = [
        "torch>=2.0.0",
        "torchvision>=0.15.0", 
        "torchaudio>=2.0.0",
        "transformers>=4.30.0",
        "datasets>=2.12.0",
        "peft>=0.4.0",
        "accelerate>=0.20.0",
        "bitsandbytes>=0.41.0"
    ]
    
    for package in ml_packages:
        try:
            print(f"📥 Installation: {package}")
            subprocess.run([str(python_path), "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur installation {package}: {e}")
            # Continue même en cas d'erreur pour certains packages
    
    return True

def install_ocr_dependencies():
    """Installation des dépendances OCR et traitement de documents"""
    print("\n📄 INSTALLATION DÉPENDANCES OCR")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    ocr_packages = [
        "PyPDF2>=3.0.0",
        "PyMuPDF>=1.23.0",
        "easyocr>=1.7.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "pdf2image>=1.16.0"
    ]
    
    for package in ocr_packages:
        try:
            print(f"📥 Installation: {package}")
            subprocess.run([str(python_path), "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur installation {package}: {e}")
    
    return True

def install_web_dependencies():
    """Installation des dépendances web et API"""
    print("\n🌐 INSTALLATION DÉPENDANCES WEB")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    web_packages = [
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "requests>=2.31.0",
        "urllib3>=1.26.0",
        "gunicorn>=21.0.0"
    ]
    
    for package in web_packages:
        try:
            print(f"📥 Installation: {package}")
            subprocess.run([str(python_path), "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation {package}: {e}")
    
    return True

def install_utility_dependencies():
    """Installation des utilitaires et outils"""
    print("\n🛠️ INSTALLATION UTILITAIRES")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    utility_packages = [
        "pandas>=2.0.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "click>=8.0.0",
        "python-dotenv>=1.0.0"
    ]
    
    for package in utility_packages:
        try:
            print(f"📥 Installation: {package}")
            subprocess.run([str(python_path), "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur installation {package}: {e}")
    
    return True

def test_installations():
    """Test des installations critiques"""
    print("\n🧪 TEST DES INSTALLATIONS")
    print("=" * 50)
    
    python_path = get_venv_python()
    
    test_imports = {
        "torch": "PyTorch",
        "transformers": "Transformers", 
        "flask": "Flask",
        "requests": "Requests",
        "PyPDF2": "PyPDF2",
        "cv2": "OpenCV",
        "yaml": "PyYAML",
        "pandas": "Pandas",
        "numpy": "NumPy"
    }
    
    success_count = 0
    
    for module, name in test_imports.items():
        try:
            result = subprocess.run([
                str(python_path), "-c", f"import {module}; print(f'{name}: OK')"
            ], capture_output=True, text=True, check=True)
            print(f"✅ {name}: Import réussi")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {name}: Erreur import - {e.stderr.strip()}")
    
    success_rate = (success_count / len(test_imports)) * 100
    print(f"\n📊 Taux de réussite imports: {success_count}/{len(test_imports)} ({success_rate:.1f}%)")
    
    return success_rate >= 80

def create_activation_script():
    """Création d'un script d'activation facile"""
    print("\n📜 CRÉATION SCRIPT D'ACTIVATION")
    print("=" * 50)
    
    # Script pour Linux/WSL
    activate_script = BASE_DIR / "activate_pgi_ia.sh"
    
    script_content = f"""#!/bin/bash
# Script d'activation environnement PGI-IA
echo "🚀 Activation environnement PGI-IA"
source {VENV_DIR}/bin/activate
export PYTHONPATH="{BASE_DIR}:$PYTHONPATH"
echo "✅ Environnement activé"
echo "📁 Répertoire: {BASE_DIR}"
echo "🐍 Python: $(which python)"
echo "📦 Pip: $(which pip)"
cd {BASE_DIR}
"""
    
    with open(activate_script, 'w') as f:
        f.write(script_content)
    
    # Rendre exécutable
    os.chmod(activate_script, 0o755)
    
    print(f"✅ Script créé: {activate_script}")
    print(f"   Usage: source {activate_script}")
    
    # Script Python pour démarrage rapide
    startup_script = BASE_DIR / "start_pgi_ia.py"
    
    startup_content = f"""#!/usr/bin/env python3
\"\"\"
Script de démarrage rapide PGI-IA
Usage: {VENV_DIR}/bin/python start_pgi_ia.py
\"\"\"

import os
import sys
import subprocess
from pathlib import Path

# Ajout du répertoire au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("🚀 DÉMARRAGE PGI-IA")
    print("=" * 40)
    
    # Vérification environnement
    print(f"🐍 Python: {{sys.executable}}")
    print(f"📁 Répertoire: {{Path.cwd()}}")
    
    # Options de démarrage
    print("\\n📋 OPTIONS DISPONIBLES:")
    print("1. Backend Flask")
    print("2. Vérification système")
    print("3. Entraînement DeepSeek")
    print("4. Interface frontend")
    
    choice = input("\\nChoisir option (1-4): ").strip()
    
    if choice == "1":
        subprocess.run([sys.executable, "backend/main.py"])
    elif choice == "2":
        subprocess.run([sys.executable, "verify_complete_system.py"])
    elif choice == "3":
        subprocess.run([sys.executable, "deepseek_finetune_english_complete.py"])
    elif choice == "4":
        print("🌐 Ouvrir frontend/index.html dans votre navigateur")
    else:
        print("Option invalide")

if __name__ == "__main__":
    main()
"""
    
    with open(startup_script, 'w') as f:
        f.write(startup_content)
    
    os.chmod(startup_script, 0o755)
    print(f"✅ Script démarrage: {startup_script}")
    
    return activate_script, startup_script

def create_requirements_file():
    """Création du fichier requirements.txt complet"""
    print("\n📝 CRÉATION REQUIREMENTS.TXT")
    print("=" * 50)
    
    requirements_content = """# PGI-IA - Dépendances complètes
# Installation: pip install -r requirements.txt

# Core ML/AI
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
transformers>=4.30.0
datasets>=2.12.0
peft>=0.4.0
accelerate>=0.20.0
bitsandbytes>=0.41.0

# OCR et traitement documents
PyPDF2>=3.0.0
PyMuPDF>=1.23.0
easyocr>=1.7.0
opencv-python>=4.8.0
Pillow>=10.0.0
pdf2image>=1.16.0

# Web et API
flask>=2.3.0
flask-cors>=4.0.0
requests>=2.31.0
urllib3>=1.26.0
gunicorn>=21.0.0

# Données et utilitaires
numpy==1.24.3
pandas>=2.0.0
pyyaml>=6.0
tqdm>=4.65.0
psutil>=5.9.0
rich>=13.0.0
click>=8.0.0
python-dotenv>=1.0.0

# Développement et outils
setuptools>=68.0.0
wheel>=0.41.0
cython>=0.29.36
"""
    
    requirements_file = BASE_DIR / "requirements_complete.txt"
    with open(requirements_file, 'w') as f:
        f.write(requirements_content)
    
    print(f"✅ Requirements créé: {requirements_file}")
    return requirements_file

def main():
    """Installation complète de l'environnement"""
    print("🔧 CONFIGURATION COMPLÈTE ENVIRONNEMENT PGI-IA")
    print("🎯 Résolution des conflits et installation complète")
    print("=" * 60)
    
    # Étapes d'installation
    steps = [
        ("Création environnement virtuel", create_clean_virtual_environment),
        ("Mise à jour pip", upgrade_pip),
        ("Installation base", install_base_dependencies),
        ("Installation ML/AI", install_ml_dependencies),
        ("Installation OCR", install_ocr_dependencies),
        ("Installation Web", install_web_dependencies),
        ("Installation utilitaires", install_utility_dependencies),
        ("Test des installations", test_installations)
    ]
    
    success_count = 0
    
    for step_name, step_function in steps:
        print(f"\n🔄 {step_name}...")
        if step_function():
            print(f"✅ {step_name} - SUCCÈS")
            success_count += 1
        else:
            print(f"❌ {step_name} - ÉCHEC")
    
    # Création des scripts d'aide
    activate_script, startup_script = create_activation_script()
    requirements_file = create_requirements_file()
    
    # Rapport final
    success_rate = (success_count / len(steps)) * 100
    
    print(f"\n📊 RÉSULTATS INSTALLATION")
    print("=" * 50)
    print(f"✅ Étapes réussies: {success_count}/{len(steps)} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🏆 INSTALLATION RÉUSSIE!")
        print("\n🚀 INSTRUCTIONS DE DÉMARRAGE:")
        print(f"1. Activer l'environnement: source {activate_script}")
        print(f"2. Ou utiliser: {VENV_DIR}/bin/python start_pgi_ia.py")
        print(f"3. Backend: {VENV_DIR}/bin/python backend/main.py")
        print(f"4. Vérification: {VENV_DIR}/bin/python verify_complete_system.py")
        
        print("\n📁 FICHIERS CRÉÉS:")
        print(f"   🔧 Environnement: {VENV_DIR}")
        print(f"   📜 Activation: {activate_script}")
        print(f"   🚀 Démarrage: {startup_script}")
        print(f"   📦 Requirements: {requirements_file}")
        
    else:
        print("⚠️ INSTALLATION PARTIELLE")
        print("🔧 Certaines dépendances peuvent nécessiter une installation manuelle")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)