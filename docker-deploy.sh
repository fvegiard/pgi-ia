#!/bin/bash
# Script de déploiement Docker pour PGI-IA

echo "🐳 Déploiement Docker PGI-IA"
echo "==========================="

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non installé !"
    exit 1
fi

# Vérifier les clés API
if [ ! -f .env ]; then
    echo "⚠️ Fichier .env manquant !"
    echo "Création du template..."
    cat > .env << EOF
# API Keys
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-sk-ccc37a109afb461989af8cf994a8bc60}
GEMINI_API_KEY=${GEMINI_API_KEY:-}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}

# Database
POSTGRES_USER=pgiia
POSTGRES_PASSWORD=pgiia
POSTGRES_DB=pgiia

# Redis
REDIS_URL=redis://redis:6379/0
EOF
    echo "✅ .env créé - Ajoute tes clés API !"
fi

# Menu
echo ""
echo "Que veux-tu faire ?"
echo "1) 🚀 Démarrer tous les services"
echo "2) 🏗️ Build les images"
echo "3) 🧪 Mode développement (avec logs)"
echo "4) 🛑 Arrêter tous les services"
echo "5) 🗑️ Clean (arrêt + suppression)"
echo "6) 📊 Voir les logs"
echo "7) 🔧 Installer nvidia-docker (GPU)"
echo ""

read -p "Choix (1-7): " choice

case $choice in
    1)
        echo "🚀 Démarrage des services..."
        docker compose up -d
        echo ""
        echo "✅ Services démarrés !"
        echo "   - Frontend : http://localhost"
        echo "   - Backend API : http://localhost:5000"
        echo "   - Gemini : http://localhost:5001"
        echo "   - DeepSeek : http://localhost:5002"
        echo "   - OCR : http://localhost:5003"
        ;;
    2)
        echo "🏗️ Build des images Docker..."
        docker compose build
        ;;
    3)
        echo "🧪 Mode développement..."
        docker compose up
        ;;
    4)
        echo "🛑 Arrêt des services..."
        docker compose down
        ;;
    5)
        echo "🗑️ Clean complet..."
        docker compose down -v --remove-orphans
        docker system prune -f
        ;;
    6)
        echo "📊 Logs des services..."
        docker compose logs -f
        ;;
    7)
        echo "🔧 Installation nvidia-docker..."
        echo "Instructions :"
        echo "1. curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg"
        echo "2. curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \\"
        echo "   sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \\"
        echo "   sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list"
        echo "3. sudo apt-get update"
        echo "4. sudo apt-get install -y nvidia-container-toolkit"
        echo "5. sudo nvidia-ctk runtime configure --runtime=docker"
        echo "6. sudo systemctl restart docker"
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac
