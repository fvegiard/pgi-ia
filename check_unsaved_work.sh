#!/bin/bash
# Script de vérification pour éviter la perte de travail PGI-IA

echo "🔍 Vérification de l'état du projet PGI-IA..."
echo "============================================"

cd /home/fvegi/dev/pgi-ia

# Vérifier les fichiers non suivis
echo -e "\n📁 Fichiers non suivis par Git:"
git ls-files --others --exclude-standard

# Vérifier les modifications non commitées
echo -e "\n✏️ Modifications non commitées:"
git status --porcelain

# Vérifier si on est à jour avec le remote
echo -e "\n🌐 État par rapport au remote:"
git fetch --dry-run 2>&1

# Lister les fichiers récemment modifiés
echo -e "\n🕒 Fichiers modifiés dans les dernières 24h:"
find . -type f -mtime -1 -not -path "./.git/*" -not -path "./venv_pgi_ia/*" | grep -E "\.(html|js|py|md)$"

# Créer un backup automatique si changements
if [[ -n $(git status --porcelain) ]]; then
    echo -e "\n⚠️ ATTENTION: Des changements non sauvegardés détectés!"
    echo "Création d'un backup automatique..."
    
    BACKUP_DIR="/home/fvegi/dev/pgi-ia-backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Copier uniquement les fichiers importants
    cp -r frontend/ "$BACKUP_DIR/" 2>/dev/null
    cp -r backend/ "$BACKUP_DIR/" 2>/dev/null
    cp *.md "$BACKUP_DIR/" 2>/dev/null
    
    echo "✅ Backup créé dans: $BACKUP_DIR"
    echo ""
    echo "🚀 Pour sauvegarder dans Git:"
    echo "   git add ."
    echo "   git commit -m \"feat: [votre message]\""
    echo "   git push origin main"
else
    echo -e "\n✅ Tout est sauvegardé dans Git!"
fi

echo -e "\n============================================"
echo "💡 Tip: Ajoutez ce script à votre crontab pour vérification automatique"
