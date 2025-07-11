#!/bin/bash
# Lanceur interactif Gemini pour PGI-IA

echo "🤖 Gemini Integration Launcher"
echo "=============================="
echo ""

cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate

# Vérifier la configuration
if [ -z "$GEMINI_API_KEY" ]; then
    source .env 2>/dev/null
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Gemini non configuré !"
    echo ""
    echo "Lance d'abord : ./setup_gemini.sh"
    echo ""
    exit 1
fi

echo "✅ Gemini configuré et prêt"
echo ""
echo "Que veux-tu faire ?"
echo ""
echo "1) 📄 Analyser un plan PDF"
echo "2) 📁 Analyser tous les PDFs d'un dossier"
echo "3) 💬 Chat avec Léa (Gemini)"
echo "4) 📊 Générer une estimation"
echo "5) 🧪 Tester Gemini"
echo "6) 🔧 Lancer Gemini CLI (terminal)"
echo ""

read -p "Choix (1-6): " choice

case $choice in
    1)
        echo ""
        echo "📄 Analyse d'un plan PDF"
        read -p "Chemin du PDF : " pdf_path
        python gemini_pgi_integration.py analyze "$pdf_path"
        ;;
    2)
        echo ""
        echo "📁 Analyse batch de PDFs"
        echo "Dossiers disponibles :"
        echo "  - plans_kahnawake/"
        echo "  - plans_alexis_nihon/"
        read -p "Dossier : " directory
        python gemini_pgi_integration.py batch "$directory"
        ;;
    3)
        echo ""
        echo "💬 Chat avec Léa (Gemini)"
        echo "Tape 'exit' pour quitter"
        echo ""
        python gemini_pgi_integration.py
        ;;
    4)
        echo ""
        echo "📊 Génération d'estimation"
        echo "Analyses disponibles :"
        ls -la */gemini_analysis.json 2>/dev/null
        read -p "Fichier JSON : " json_file
        # TODO: Implémenter
        ;;
    5)
        echo ""
        echo "🧪 Test de Gemini..."
        python gemini_manager.py
        ;;
    6)
        echo ""
        echo "🔧 Lancement de Gemini CLI..."
        if [ -d "/home/fvegi/dev/gemini-cli" ]; then
            cd /home/fvegi/dev/gemini-cli
            npm start
        else
            echo "❌ Gemini CLI non installé"
            echo "Installation en cours..."
            cd /home/fvegi/dev
            git clone https://github.com/google-gemini/gemini-cli.git
            cd gemini-cli
            npm install
            npm start
        fi
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac
