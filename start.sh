#!/bin/bash

# Script de démarrage PGI-IA
# Usage: ./start.sh [backend|frontend|all]

set -e

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 PGI-IA - Démarrage du système${NC}"

# Fonction pour démarrer le backend
start_backend() {
    echo -e "${YELLOW}📦 Démarrage du backend...${NC}"
    
    cd backend
    
    # Créer environnement virtuel si n'existe pas
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
        python3 -m venv venv
    fi
    
    # Activer venv et installer dépendances
    source venv/bin/activate
    
    # Installer requirements si nécessaire
    if [ ! -f ".deps_installed" ]; then
        echo -e "${YELLOW}Installation des dépendances...${NC}"
        pip install --upgrade pip
        pip install -r requirements.txt
        touch .deps_installed
    fi
    
    # Créer dossiers nécessaires
    mkdir -p uploads data logs
    
    # Démarrer FastAPI
    echo -e "${GREEN}✅ Backend prêt sur http://localhost:8000${NC}"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Fonction pour démarrer le frontend
start_frontend() {
    echo -e "${YELLOW}🎨 Démarrage du frontend...${NC}"
    
    cd frontend
    
    # Installer dépendances si nécessaire
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installation des dépendances npm...${NC}"
        npm install
    fi
    
    # Démarrer Vite
    echo -e "${GREEN}✅ Frontend prêt sur http://localhost:5173${NC}"
    npm run dev
}

# Fonction pour démarrer les deux
start_all() {
    # Démarrer backend en arrière-plan
    (cd backend && start_backend) &
    BACKEND_PID=$!
    
    # Attendre un peu que le backend démarre
    sleep 5
    
    # Démarrer frontend
    start_frontend
    
    # Attendre les processus
    wait $BACKEND_PID
}

# Parser arguments
case "${1:-all}" in
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    all)
        start_all
        ;;
    *)
        echo -e "${RED}Usage: $0 [backend|frontend|all]${NC}"
        exit 1
        ;;
esac