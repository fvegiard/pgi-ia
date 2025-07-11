#!/bin/bash
# Lanceur rapide pour Google Session dans PGI-IA

echo "🔐 Google Session Manager pour PGI-IA"
echo "===================================="
echo ""
echo "Que veux-tu faire ?"
echo "1) Configurer les cookies Google"
echo "2) Tester l'authentification"
echo "3) Rechercher des PDFs dans Drive"
echo "4) Lancer PGI-IA avec Google intégré"
echo ""

read -p "Choix (1-4): " choice

cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate

case $choice in
    1)
        echo "🔧 Configuration des cookies..."
        python setup_google_session.py
        ;;
    2)
        echo "🧪 Test de l'authentification..."
        python google_session_manager.py
        ;;
    3)
        echo "🔍 Recherche de PDFs..."
        python google_pgi_integration.py
        ;;
    4)
        echo "🚀 Démarrage de PGI-IA avec Google..."
        source setup_env.sh
        python backend/main.py
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac
