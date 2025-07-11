#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Installation du Gemini CLI (@google/gemini-cli)"

# Si gemini est déjà présent, on sort
if command -v gemini >/dev/null 2>&1; then
  echo "✅ gemini CLI déjà installé (version: $(gemini --version))"
  exit 0
fi

# Vérifier que npm est installé
if ! command -v npm >/dev/null 2>&1; then
  echo "❌ npm non trouvé. Installe Node.js et npm : https://nodejs.org/"
  exit 1
fi

echo "ℹ️  npm version: $(npm --version)"
echo "⚙️  Tentative d'installation globale @google/gemini-cli"

if npm install -g @google/gemini-cli; then
  echo "✅ Installation globale réussie : gemini version $(gemini --version)"
  exit 0
else
  echo "⚠️ Installation globale échouée, fallback via npx (pas de sudo requis)"
  echo "→ Pour une utilisation temporaire :"
  echo "     alias gemini='npx --yes @google/gemini-cli'"
  echo "     gemini --version"
  exit 1
fi