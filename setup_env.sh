#!/bin/bash
# Script de configuration des variables d'environnement pour PGI-IA

# Charger les variables depuis le fichier .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Variables d'environnement chargées depuis .env"
else
    echo "⚠️ Fichier .env non trouvé"
fi

# Afficher l'état des clés API
echo ""
echo "🔑 État des clés API:"
echo "--------------------"

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "✅ OPENAI_API_KEY: ${OPENAI_API_KEY:0:20}..."
else
    echo "❌ OPENAI_API_KEY: Non configurée"
fi

if [ ! -z "$DEEPSEEK_API_KEY" ]; then
    echo "✅ DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY:0:20}..."
else
    echo "❌ DEEPSEEK_API_KEY: Non configurée"
fi

if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo "✅ ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:20}..."
else
    echo "⚠️ ANTHROPIC_API_KEY: Non configurée (optionnel)"
fi

if [ ! -z "$GOOGLE_API_KEY" ]; then
    echo "✅ GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:20}..."
else
    echo "⚠️ GOOGLE_API_KEY: Non configurée (optionnel)"
fi

echo ""
