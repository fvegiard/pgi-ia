#!/bin/bash
# Script de synchronisation WSL → Windows pour PGI-IA

echo "🔄 Synchronisation PGI-IA : WSL → Windows"
echo "========================================"

# Dossiers source et destination
WSL_DIR="/home/fvegi/dev/pgi-ia"
WIN_DIR="/mnt/c/Users/fvegi/dev/pgi-ia"
WIN_FRONTEND_DIR="/mnt/c/Users/fvegi/dev/pgi-ia-frontend"

# Vérifier que les dossiers existent
if [ ! -d "$WSL_DIR" ]; then
    echo "❌ Erreur : Dossier WSL non trouvé : $WSL_DIR"
    exit 1
fi

if [ ! -d "$WIN_DIR" ]; then
    echo "❌ Erreur : Dossier Windows non trouvé : $WIN_DIR"
    exit 1
fi

# Synchroniser les fichiers importants
echo "📁 Synchronisation du dossier principal..."

# Frontend
echo "  → Copie des fichiers frontend..."
cp -r $WSL_DIR/frontend/* $WIN_DIR/frontend/ 2>/dev/null

# Documentation
echo "  → Copie de la documentation..."
cp $WSL_DIR/*.md $WIN_DIR/ 2>/dev/null

# Scripts
echo "  → Copie des scripts..."
cp $WSL_DIR/*.sh $WIN_DIR/ 2>/dev/null

# Backend (sans venv)
echo "  → Copie du backend..."
rsync -av --exclude='venv_pgi_ia' --exclude='__pycache__' \
    $WSL_DIR/backend/ $WIN_DIR/backend/ 2>/dev/null

# Si le dossier frontend séparé existe
if [ -d "$WIN_FRONTEND_DIR" ]; then
    echo ""
    echo "📁 Synchronisation du dossier frontend séparé..."
    cp $WSL_DIR/frontend/* $WIN_FRONTEND_DIR/ 2>/dev/null
fi

echo ""
echo "✅ Synchronisation terminée !"
echo ""
echo "📌 Fichiers dashboard ajoutés :"
echo "  - frontend/dashboard.html"
echo "  - frontend/dashboard.js"
echo "  - start_dashboard.sh"
echo ""
echo "💡 Pour tester le nouveau dashboard :"
echo "  1. Ouvrir PowerShell dans C:\Users\fvegi\dev\pgi-ia"
echo "  2. Lancer : python -m http.server 8080"
echo "  3. Ouvrir : http://localhost:8080/frontend/dashboard.html"