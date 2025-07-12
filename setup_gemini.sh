#!/bin/bash
# Installation et configuration de Gemini pour PGI-IA

echo "🚀 Configuration de Gemini pour PGI-IA"
echo "======================================"

# Vérifier si google-generativeai est installé
echo "📦 Installation des dépendances Python..."
cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate
pip install google-generativeai > /dev/null 2>&1

# Vérifier la clé API
if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo ""
    echo "⚠️  Aucune clé API Gemini détectée !"
    echo ""
    echo "🔑 Pour obtenir une clé GRATUITE :"
    echo "   1. Va sur : https://makersuite.google.com/app/apikey"
    echo "   2. Clique sur 'Create API Key'"
    echo "   3. Copie la clé (format : AIzaSy...)"
    echo ""
    read -p "Colle ta clé API Gemini ici : " api_key
    
    if [ ! -z "$api_key" ]; then
        # Ajouter au .env
        echo "GEMINI_API_KEY=$api_key" >> /home/fvegi/dev/pgi-ia/.env
        export GEMINI_API_KEY=$api_key
        echo "✅ Clé API sauvegardée dans .env"
    fi
else
    echo "✅ Clé API Gemini détectée"
fi

# Installation de Gemini CLI (optionnel)
if [ ! -d "/home/fvegi/dev/gemini-cli" ]; then
    echo ""
    echo "📥 Installation de Gemini CLI..."
    cd /home/fvegi/dev
    
    # Si le clone est toujours en cours, on attend
    if pgrep -f "git clone.*gemini-cli" > /dev/null; then
        echo "⏳ Clone en cours, patientez..."
        wait
    fi
    
    if [ -d "gemini-cli" ]; then
        cd gemini-cli
        npm install > /dev/null 2>&1
        echo "✅ Gemini CLI installé"
    fi
fi

# Test de Gemini
echo ""
echo "🧪 Test de Gemini..."
cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate
python -c "
from gemini_manager import GeminiManager
gemini = GeminiManager()
if gemini.model:
    print('✅ Gemini fonctionnel !')
    response = gemini.chat('Dis bonjour en une phrase')
    print(f'Gemini dit : {response}')
else:
    print('❌ Configuration requise')
"

echo ""
echo "📋 Commandes disponibles :"
echo "   - python gemini_manager.py         # Test Gemini"
echo "   - ./gemini_integration_launcher.sh # Menu interactif"
echo ""
