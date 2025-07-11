#!/bin/bash
# Script OBLIGATOIRE à exécuter AVANT tout travail
# GitHub First Policy Enforcement

echo "🌐 GITHUB FIRST CHECK - OBLIGATOIRE"
echo "===================================="

# 1. Pull latest
echo -e "\n📥 Synchronisation avec GitHub..."
git pull origin main
PULL_STATUS=$?

if [ $PULL_STATUS -ne 0 ]; then
    echo "❌ ERREUR: Impossible de synchroniser avec GitHub!"
    echo "⚠️  Résoudre les conflits avant de continuer"
    exit 1
fi

# 2. Afficher statut
echo -e "\n📝 Statut local:"
git status --short

# 3. Vérifier si des fichiers non committés
UNCOMMITTED=$(git status --porcelain | wc -l)
if [ $UNCOMMITTED -gt 0 ]; then
    echo -e "\n⚠️  ATTENTION: $UNCOMMITTED fichier(s) non commité(s)!"
    echo "Considérer commit + push avant modifications"
fi

# 4. Afficher derniers commits
echo -e "\n📜 Derniers commits GitHub:"
git log --oneline -5

# 5. Test connexion API GitHub
echo -e "\n🔗 Test connexion API GitHub..."
API_RESPONSE=$(curl -s "https://api.github.com/repos/fvegiard/pgi-ia" | grep "full_name")
if [ -z "$API_RESPONSE" ]; then
    echo "❌ ERREUR: API GitHub non accessible!"
    exit 1
else
    echo "✅ API GitHub connectée"
fi

# 6. Afficher fichiers importants
echo -e "\n📁 Fichiers critiques sur GitHub:"
curl -s "https://api.github.com/repos/fvegiard/pgi-ia/contents/frontend" | grep "name" | grep -E "dashboard|index" | head -5
curl -s "https://api.github.com/repos/fvegiard/pgi-ia/contents/backend" | grep "name" | grep -E "main|system|manager" | head -5

echo -e "\n✅ GitHub First Check terminé!"
echo "💡 Rappel: TOUJOURS vérifier GitHub avant création de fichier"
echo "===================================="