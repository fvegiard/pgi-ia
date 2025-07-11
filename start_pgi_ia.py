#!/usr/bin/env python3
"""
Script de démarrage rapide PGI-IA
Usage: /home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python start_pgi_ia.py
"""

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
    print(f"🐍 Python: {sys.executable}")
    print(f"📁 Répertoire: {Path.cwd()}")
    
    # Options de démarrage
    print("\n📋 OPTIONS DISPONIBLES:")
    print("1. Backend Flask")
    print("2. Vérification système")
    print("3. Entraînement DeepSeek")
    print("4. Interface frontend")
    
    choice = input("\nChoisir option (1-4): ").strip()
    
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
