# 🔧 Configuration Claude Desktop pour PGI-IA

## Installation rapide dans Claude Desktop

### 1. Cloner le projet
```bash
# Dans Claude Desktop, exécutez :
cd /mnt/c/Users/fvegi/dev
git clone https://github.com/fvegiard/pgi-ia.git
cd pgi-ia
```

### 2. Créer l'environnement Python
```bash
# Créer environnement virtuel
python -m venv venv_pgi_ia

# Activer (Windows WSL)
source venv_pgi_ia/bin/activate

# Installer dépendances
pip install -r requirements_complete.txt
```

### 3. Configuration des APIs
```bash
# Créer fichier .env ou exporter directement
export OPENAI_API_KEY="sk-..."
export DEEPSEEK_API_KEY="sk-..."
```

### 4. Démarrer le système

#### Backend Flask
```bash
python backend/main.py
```

#### Frontend (dans navigateur)
Ouvrir : `file:///C:/Users/fvegi/dev/pgi-ia/frontend/index.html`

### 5. Commandes utiles pour Claude Desktop

#### Vérification système
```bash
python verify_complete_system.py
```

#### Audits qualité
```bash
# Audit technique
python audit_deepseek.py

# Audit UX
python audit_justina.py
```

#### Entraînement DeepSeek avec plans
```bash
# Placer d'abord vos PDFs dans :
# - plans_kahnawake/
# - plans_alexis_nihon/

# Lancer l'entraînement
python deepseek_finetune_english_complete.py
```

## 📋 Structure pour Claude Desktop

```
C:\Users\fvegi\dev\pgi-ia\
├── backend\              # API Flask (port 5000)
├── frontend\             # Interface web Tailwind
├── plans_kahnawake\      # Déposer 300+ PDFs ici
├── plans_alexis_nihon\   # Plans Alexis-Nihon
├── venv_pgi_ia\          # Environnement Python
└── *.py                  # Scripts d'entraînement
```

## 🔄 Workflow Claude Desktop

### Pour les modifications

1. **Faire les changements dans Claude Desktop**
```bash
# Éditer les fichiers
# Tester localement
```

2. **Commit et push**
```bash
git add .
git commit -m "Description des changements"
git push origin main
```

3. **Synchroniser dans WSL** (si nécessaire)
```bash
# Dans WSL
cd /home/fvegi/dev/pgi-ia
git pull origin main
```

### Pour l'entraînement GPU

Si votre GPU est dans WSL :
```bash
# Copier les plans vers WSL
cp -r /mnt/c/Users/fvegi/dev/pgi-ia/plans_* /home/fvegi/dev/pgi-ia/

# Lancer l'entraînement dans WSL
cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate
python deepseek_finetune_english_complete.py
```

## 🎯 Cas d'usage Claude Desktop

### 1. Développement Frontend
- Éditer `frontend/index.html` et `script.js`
- Prévisualiser directement dans Windows
- Push vers GitHub

### 2. Ajout de nouvelles directives
- Modifier `frontend/script.js` (projectsData)
- Tester localement
- Commit et push

### 3. Traitement de plans PDF
- Déposer PDFs dans `plans_kahnawake/`
- Lancer le script d'extraction
- Visualiser les résultats

### 4. Fine-tuning DeepSeek
- Préparer dataset dans Claude Desktop
- Transférer vers WSL si GPU là-bas
- Ou utiliser CPU dans Windows

## 🔧 Démarrage automatique complet

Dans Claude Desktop :
```bash
python start_all_services.py
```

Cela lance :
- ✅ Backend Flask
- ✅ Vérifications système
- ✅ Instructions frontend
- ✅ Monitoring services

## 📝 Notes importantes

1. **Chemins Windows vs WSL**
   - Windows : `C:\Users\fvegi\dev\pgi-ia`
   - WSL : `/home/fvegi/dev/pgi-ia`
   - Claude Desktop : `/mnt/c/Users/fvegi/dev/pgi-ia`

2. **Port Backend**
   - Toujours sur `http://localhost:5000`
   - Accessible depuis Windows et WSL

3. **GPU pour entraînement**
   - Vérifiez où est votre GPU (WSL ou Windows)
   - Adaptez l'emplacement d'exécution

4. **Synchronisation Git**
   - Toujours pull avant de commencer
   - Push après chaque session

## 🚀 Commande rapide tout-en-un

```bash
# Dans Claude Desktop
cd /mnt/c/Users/fvegi/dev/pgi-ia && \
git pull origin main && \
source venv_pgi_ia/bin/activate && \
python start_all_services.py
```

---
*Ce guide est spécifique à Claude Desktop pour le projet PGI-IA*