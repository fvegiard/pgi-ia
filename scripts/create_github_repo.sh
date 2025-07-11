#!/usr/bin/env bash
set -euo pipefail

# Script d'automatisation : création du repository GitHub et push initial

# Vérifier la présence du token GitHub
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Erreur : veuillez exporter votre Personal Access Token GitHub dans GITHUB_TOKEN."
  echo "Exemple : export GITHUB_TOKEN=ghp_xxx"
  exit 1
fi

# Lecture des paramètres utilisateur/organisation et nom du repo
read -r -p "Utilisateur ou organisation GitHub (default: $(git config user.name)): " ORG
ORG=${ORG:-$(git config user.name)}
read -r -p "Nom du repository (default: pgi-ia): " REPO
REPO=${REPO:-pgi-ia}

# Création via API GitHub (orga puis user)
echo "Création du repository ${ORG}/${REPO} sur GitHub..."
curl -sS -H "Authorization: token $GITHUB_TOKEN" \
     -d "{\"name\":\"$REPO\",\"private\":false}" \
     https://api.github.com/orgs/${ORG}/repos || \
  (
    echo "⚠️  Création via organisation échouée, tentative sur l'utilisateur courant...";
    curl -sS -H "Authorization: token $GITHUB_TOKEN" \
         -d "{\"name\":\"$REPO\",\"private\":false}" \
         https://api.github.com/user/repos
  )

# Liaison du remote et push
echo "Initialisation du dépôt local et push sur GitHub..."
git remote add origin "git@github.com:${ORG}/${REPO}.git"
git branch -M main
git push -u origin main

echo "✅ Repository ${ORG}/${REPO} créé et initial commit poussé."