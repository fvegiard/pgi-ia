#!/bin/bash
# Script de lancement du dashboard PGI-IA

echo "🚀 Lancement du dashboard PGI-IA..."
echo "================================="

# Vérifier si Python est disponible
if command -v python3 &> /dev/null; then
    echo "✅ Démarrage du serveur HTTP local..."
    echo ""
    echo "📌 Dashboard disponible sur: http://localhost:8080/dashboard.html"
    echo "📌 Interface dark (ancienne): http://localhost:8080/index.html"
    echo ""
    echo "Appuyez sur Ctrl+C pour arrêter le serveur"
    echo ""
    cd /home/fvegi/dev/pgi-ia/frontend
    python3 -m http.server 8080
else
    echo "❌ Python3 non trouvé. Installation requise."
    echo "Essayez: sudo apt install python3"
fi