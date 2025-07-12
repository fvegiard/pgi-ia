#!/bin/bash
# Script pour configurer l'accès sudo avec le mot de passe 12345
# ATTENTION: Ceci est pour un environnement de développement uniquement

echo "Configuration de l'accès sudo pour Claude Code..."

# Créer un fichier de configuration sudoers temporaire
SUDO_FILE="/tmp/claude_code_sudo"
cat > $SUDO_FILE << 'EOF'
# Configuration sudo pour Claude Code - Environnement dev
fvegi ALL=(ALL) NOPASSWD: ALL
EOF

echo "📝 Configuration créée. Pour activer:"
echo "1. Exécutez: sudo visudo"
echo "2. Ajoutez cette ligne à la fin: fvegi ALL=(ALL) NOPASSWD: ALL"
echo "3. Sauvegardez et quittez"
echo ""
echo "⚠️  SÉCURITÉ: Ceci donne un accès sudo complet sans mot de passe!"
echo "🔒 Alternative plus sûre: utiliser le mot de passe 12345"
echo ""
echo "Pour configurer avec mot de passe:"
echo "sudo passwd fvegi"
echo "Puis entrez: 12345"