#!/bin/bash
# Script de test du backend avec module emails

echo "🚀 Test du backend PGI-IA avec module Emails"
echo "==========================================="

# Vérifier l'environnement virtuel
if [ ! -d "venv_pgi_ia" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "Créez-le avec: python3 -m venv venv_pgi_ia"
    exit 1
fi

# Activer l'environnement
echo "✅ Activation de l'environnement virtuel..."
source venv_pgi_ia/bin/activate

# Charger les variables d'environnement
echo "✅ Chargement des variables d'environnement..."
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Fichier .env non trouvé"
fi

# Installer les dépendances manquantes si nécessaire
echo "✅ Vérification des dépendances..."
pip install -q python-dotenv 2>/dev/null

# Démarrer le backend en arrière-plan
echo ""
echo "🚀 Démarrage du backend Flask..."
python backend/main.py &
BACKEND_PID=$!

# Attendre que le serveur démarre
echo "⏳ Attente du démarrage du serveur..."
sleep 3

# Tester les endpoints
echo ""
echo "🧪 Test des endpoints email..."
echo "================================"

# Test 1: Liste des emails
echo "1️⃣ GET /api/emails"
curl -s http://localhost:5000/api/emails | python -m json.tool | head -20

# Test 2: Emails non lus
echo ""
echo "2️⃣ GET /api/emails/unread"
curl -s http://localhost:5000/api/emails/unread | python -m json.tool

# Test 3: Stats
echo ""
echo "3️⃣ GET /api/emails/stats"
curl -s http://localhost:5000/api/emails/stats | python -m json.tool

# Test 4: Classification d'un email
echo ""
echo "4️⃣ POST /api/emails/classify"
curl -s -X POST http://localhost:5000/api/emails/classify \
  -H "Content-Type: application/json" \
  -d '{
    "from": "test@example.com",
    "subject": "Directive CD-999 - Test classification",
    "body": "Voici une directive de test pour le projet Kahnawake. Impact: 5000$",
    "attachments": []
  }' | python -m json.tool

echo ""
echo "================================"
echo "✅ Tests terminés"
echo ""
echo "📌 Backend en cours d'exécution (PID: $BACKEND_PID)"
echo "📌 Dashboard: Ouvrir frontend/dashboard.html"
echo "📌 Pour arrêter: kill $BACKEND_PID"
echo ""
echo "💡 Pour intégrer avec le frontend:"
echo "   - Modifier dashboard.js pour utiliser les vrais endpoints"
echo "   - Remplacer les données mockées par fetch()"
echo ""