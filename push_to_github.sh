#!/bin/bash
# Helper script pour push vers GitHub

echo "🚀 Push vers GitHub"
echo "=================="

# Vérifier s'il y a des changements
if [[ $(git status --porcelain) ]]; then
    echo "📝 Changements détectés, création commit..."
    git add .
    git commit -m "🔄 Mise à jour automatique $(date +%Y-%m-%d)"
fi

# Push
echo "📤 Push vers GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Push réussi!"
else
    echo "❌ Erreur push - Vérifiez votre authentification"
    echo ""
    echo "Utilisez une des options ci-dessus pour configurer l'authentification"
fi
