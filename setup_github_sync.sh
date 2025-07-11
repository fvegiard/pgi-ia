#!/bin/bash
# Configuration GitHub pour synchronisation facile
# Permet de pousser vers GitHub depuis WSL

echo "🔧 CONFIGURATION GITHUB SYNC"
echo "============================"
echo ""
echo "Ce script aide à configurer Git pour synchroniser avec GitHub"
echo ""

# Option 1: Via GitHub Desktop (Windows)
echo "📋 OPTION 1: Via GitHub Desktop (Windows)"
echo "========================================="
echo "1. Copiez le dossier complet vers Windows:"
echo "   cp -r /home/fvegi/dev/pgi-ia /mnt/c/Users/fvegi/dev/"
echo ""
echo "2. Dans GitHub Desktop:"
echo "   - File > Add Local Repository"
echo "   - Sélectionnez: C:\\Users\\fvegi\\dev\\pgi-ia"
echo "   - Commit & Push"
echo ""

# Option 2: Personal Access Token
echo "📋 OPTION 2: Personal Access Token (Recommandé)"
echo "=============================================="
echo "1. Allez sur GitHub.com > Settings > Developer settings > Personal access tokens"
echo "2. Générez un nouveau token avec permissions 'repo'"
echo "3. Copiez le token"
echo ""
echo "4. Configurez Git avec le token:"
echo "   git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/pgi-ia.git"
echo ""

# Option 3: SSH Key
echo "📋 OPTION 3: Clé SSH"
echo "==================="
echo "1. Générez une clé SSH (si pas déjà fait):"
echo "   ssh-keygen -t ed25519 -C \"your-email@example.com\""
echo ""
echo "2. Ajoutez la clé publique à GitHub:"
echo "   cat ~/.ssh/id_ed25519.pub"
echo "   (Copiez et ajoutez dans GitHub > Settings > SSH Keys)"
echo ""
echo "3. Changez l'URL remote:"
echo "   git remote set-url origin git@github.com:YOUR_USERNAME/pgi-ia.git"
echo ""

# Commandes actuelles
echo "📊 STATUT ACTUEL"
echo "================"
echo "Remote actuel:"
git remote -v
echo ""
echo "Dernier commit:"
git log --oneline -1
echo ""

# Script helper pour push
cat > push_to_github.sh << 'EOF'
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
EOF

chmod +x push_to_github.sh

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "📜 Script helper créé: ./push_to_github.sh"
echo "   Utilisez ce script pour pusher facilement vers GitHub"
echo ""