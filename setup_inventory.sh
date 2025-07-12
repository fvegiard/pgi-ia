#!/bin/bash
# Script de setup et inventaire complet PGI-IA
# Créé automatiquement le $(date)

echo "🚀 SETUP ET INVENTAIRE PGI-IA"
echo "=============================="
echo ""

# Fonction pour vérifier et créer si nécessaire
check_and_create() {
    local file=$1
    local description=$2
    if [ -f "$file" ]; then
        echo "✅ $description existe"
    else
        echo "❌ $description manquant"
        echo "$file" >> missing_files.txt
    fi
}

# 1. Inventaire des fichiers
echo "📄 INVENTAIRE DES FICHIERS CLÉS"
echo "--------------------------------"

# Scripts mentionnés dans la doc
check_and_create "verify_complete_system.py" "Script vérification système"
check_and_create "audit_deepseek.py" "Audit DeepSeek"
check_and_create "audit_justina.py" "Audit Justina"
check_and_create "deepseek_finetune_english_complete.py" "Entraînement DeepSeek"
check_and_create "start_all_services.py" "Démarrage tous services"

echo ""
echo "📁 STRUCTURE DES RÉPERTOIRES"
echo "----------------------------"
for dir in backend frontend config data scripts tests plans_kahnawake plans_alexis_nihon; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -type f | wc -l)
        echo "✅ /$dir ($count fichiers)"
    else
        echo "❌ /$dir manquant"
    fi
done

echo ""
echo "🔑 CONFIGURATION APIS"
echo "---------------------"
if [ -f ".env" ]; then
    echo "✅ Fichier .env trouvé"
else
    echo "❌ Fichier .env manquant"
    echo "   → Copier backend/.env.example vers .env"
fi

echo ""
echo "🐍 ENVIRONNEMENT PYTHON"
echo "-----------------------"
if [ -d "venv_pgi_ia" ]; then
    echo "✅ Environnement virtuel présent"
else
    echo "❌ Environnement virtuel manquant"
    echo "   → Créer avec: python3 -m venv venv_pgi_ia"
fi

echo ""
echo "📊 RÉSUMÉ GIT"
echo "-------------"
echo "Fichiers modifiés: $(git status --porcelain | grep '^ M' | wc -l)"
echo "Fichiers non suivis: $(git status --porcelain | grep '^??' | wc -l)"
echo "Branche actuelle: $(git branch --show-current)"

echo ""
echo "🔧 ACTIONS RECOMMANDÉES"
echo "-----------------------"
echo "1. Créer environnement virtuel :"
echo "   python3 -m venv venv_pgi_ia"
echo "   source venv_pgi_ia/bin/activate"
echo "   pip install -r backend/requirements.txt"
echo ""
echo "2. Configurer les APIs :"
echo "   cp backend/.env.example .env"
echo "   # Éditer .env avec vos clés API"
echo ""
echo "3. Commit des changements :"
echo "   git add ."
echo "   git commit -m 'Ajout documentation et setup'"
echo "   git push origin main"
echo ""
echo "4. Démarrer le backend :"
echo "   source venv_pgi_ia/bin/activate"
echo "   python backend/main.py"

# Créer un fichier de statut JSON
cat > system_status.json <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "python_version": "$(python3 --version 2>&1)",
  "git_status": {
    "modified": $(git status --porcelain | grep '^ M' | wc -l),
    "untracked": $(git status --porcelain | grep '^??' | wc -l),
    "branch": "$(git branch --show-current)"
  },
  "structure": {
    "backend": $([ -d "backend" ] && echo "true" || echo "false"),
    "frontend": $([ -d "frontend" ] && echo "true" || echo "false"),
    "venv": $([ -d "venv_pgi_ia" ] && echo "true" || echo "false"),
    "env_file": $([ -f ".env" ] && echo "true" || echo "false")
  }
}
EOF

echo ""
echo "✨ Inventaire terminé ! Résultats dans :"
echo "   - system_status.json"
echo "   - missing_files.txt (si des fichiers manquent)"
