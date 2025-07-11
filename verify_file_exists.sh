#!/bin/bash
# Vérifie si un fichier existe sur GitHub AVANT création
# Usage: ./verify_file_exists.sh path/to/file

if [ -z "$1" ]; then
    echo "❌ Usage: $0 <path/to/file>"
    echo "Exemple: $0 frontend/dashboard.html"
    exit 1
fi

FILE_PATH=$1
API_URL="https://api.github.com/repos/fvegiard/pgi-ia/contents/$FILE_PATH"

echo "🔍 Vérification sur GitHub: $FILE_PATH"
echo "===================================="

# Faire la requête
RESPONSE=$(curl -s "$API_URL")

# Vérifier si fichier existe
if echo "$RESPONSE" | grep -q "\"name\""; then
    echo "✅ FICHIER EXISTE sur GitHub!"
    echo ""
    
    # Extraire infos
    NAME=$(echo "$RESPONSE" | grep -o '"name":"[^"]*' | cut -d'"' -f4)
    SIZE=$(echo "$RESPONSE" | grep -o '"size":[0-9]*' | cut -d':' -f2)
    SHA=$(echo "$RESPONSE" | grep -o '"sha":"[^"]*' | cut -d'"' -f4)
    
    echo "📄 Nom: $NAME"
    echo "📏 Taille: $SIZE bytes"
    echo "🔑 SHA: ${SHA:0:7}..."
    echo ""
    echo "⚠️  ACTION REQUISE: Utiliser Edit/Read au lieu de Write!"
    echo "💡 Commande: Read $FILE_PATH"
    
    # Afficher lien GitHub
    echo ""
    echo "🔗 Voir sur GitHub:"
    echo "https://github.com/fvegiard/pgi-ia/blob/main/$FILE_PATH"
    
    exit 0
else
    # Vérifier si c'est une erreur 404 ou autre
    if echo "$RESPONSE" | grep -q "Not Found"; then
        echo "❌ Fichier n'existe PAS sur GitHub"
        echo "✅ Création autorisée avec Write"
        
        # Suggérer vérification du dossier parent
        PARENT_DIR=$(dirname "$FILE_PATH")
        echo ""
        echo "💡 Vérifier d'abord le dossier parent:"
        echo "./verify_file_exists.sh $PARENT_DIR"
    else
        echo "⚠️  Erreur lors de la vérification:"
        echo "$RESPONSE" | head -3
    fi
    
    exit 1
fi