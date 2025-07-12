#!/bin/bash
# Script d'activation environnement PGI-IA
echo "🚀 Activation environnement PGI-IA"
source /home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/activate
export PYTHONPATH="/home/fvegi/dev/pgi-ia:$PYTHONPATH"
echo "✅ Environnement activé"
echo "📁 Répertoire: /home/fvegi/dev/pgi-ia"
echo "🐍 Python: $(which python)"
echo "📦 Pip: $(which pip)"
cd /home/fvegi/dev/pgi-ia
