#!/usr/bin/env bash
set -euo pipefail

# Demo test des fichiers de démo Gemini depuis Desktop OneDrive
OWN_DESKTOP="/mnt/c/Users/fvegi/OneDrive/Desktop"
FILES=(
  "$OWN_DESKTOP/PGI-IA  Plan d'Affaires et Feuille.txt"
  "$OWN_DESKTOP/suivis directive alexis nihon.html"
  "$OWN_DESKTOP/Kahnawake suivis directive.html"
)

echo "🔍 Test des fichiers Gemini de OneDrive Desktop"
for f in "${FILES[@]}"; do
  echo -e "\n=== $(basename "$f") ==="
  if [[ -f "$f" ]]; then
    # Si PDF, lancer parse_directive
    if [[ "${f,,}" == *.pdf ]]; then
      echo "-> Exécution parse_directive.py"
      scripts/parse_directive.py "$f"
    else
      echo "-> Extraction du contenu (50 premières lignes)"
      sed -n '1,50p' "$f"
    fi
  else
    echo "Fichier introuvable: $f"
  fi
done