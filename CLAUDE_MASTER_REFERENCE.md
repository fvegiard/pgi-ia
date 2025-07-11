# 🎯 CLAUDE MASTER REFERENCE - Session PGI-IA
# DERNIÈRE MISE À JOUR: 11 Juillet 2025 - 13:20 (Claude Code WSL)
# Projet: PGI-IA v4.1 - Progiciel de Gestion Intégré avec IA
# ⚠️ RÈGLE: Toute IA (Claude Code/Claude Desktop) DOIT écrire ici avec date/heure

## 📊 ÉTAT ACTUEL DU SYSTÈME

### ✅ Ce qui fonctionne
- **Environnement Python** : venv_pgi_ia activé, Python 3.12.3
- **GPU** : RTX 4060 détecté, 11.7GB mémoire
- **Backend Flask** : Prêt sur port 5000
- **Frontend** : Interface Tailwind CSS complète
- **DeepSeek API** : ✅ Configurée (sk-ccc37a109afb461989af8cf994a8bc60)
- **Structure** : Tous les fichiers critiques présents

### ❌ APIs manquantes (recherche exhaustive effectuée)
- **OpenAI** : Non trouvée (seulement sk-xxxxxxxx masquée)
- **Anthropic** : Non trouvée (Claude Desktop installé sans clé)
- **Google** : Non trouvée (dossiers présents sans clé)

---

## 📝 JOURNAL DES SESSIONS IA

### 🤖 SESSION Claude Code WSL - 11/07/2025 13:38
**Travail effectué:**
- ✅ Système d'emails intelligent complet créé
- ✅ Interface dashboard moderne avec onglet Emails + badge rouge
- ✅ DeepSeek email classifier spécialisé électrique  
- ✅ Endpoints API: /api/emails, /api/emails/unread, etc.
- ✅ Correction bug graphiques Chart.js (resize infini)
- ✅ Backup complet système + documentation continuité
- ✅ Tests intégrité 91.5% - Système opérationnel
- ✅ Git synchronisé, commit d107504 pushé

**Fichiers créés/modifiés:**
- backend/email_classifier_deepseek.py
- backend/email_endpoints.py  
- DEEPSEEK_EMAIL_INTEGRATION.md
- FIX_CHARTS_RESIZE.md
- ETAT_SYSTEM_PARFAIT_CONTINUITE.md
- dashboard.html, dashboard.js (correction charts)

- ✅ Système logging universel Claude Code/Desktop créé
- ✅ **ANALYSE COMPLÈTE PHASE RÉALISTE EFFECTUÉE**

**Besoins utilisateur identifiés:**
- 🎙️ Système réunions: Audio → Transcription → IA analyse par projet
- 📝 Notes intelligentes: Note → IA reformulation → Approbation → Stockage
- 🗺️ Photos GPS: iPhone photos → GPS extraction → Markers sur plan principal
- 🏗️ Pipeline 2D→3D: Email/Drop → PDF→CAD→3D → Chemins canalisations IA

**Composants critiques manquants:**
- Base données étendue (projets, meetings, notes, photos_gps, cad_files)
- APIs externes: Whisper (audio), Maps (GPS), CAD conversion, 3D engine
- Interface 3D interactive pour édition chemins canalisations
- Mobile PWA pour upload photos chantier

**PRIORITÉ 1 (démarrer maintenant):**
1. Base données SQLite étendue - Foundation everything
2. Système notes par projet - Usage quotidien  
3. Upload photos + extraction GPS - Workflow chantier
4. Pipeline email → CAD basique - Core business

- ✅ Vérification unicité CLAUDE_MASTER_REFERENCE.md (1 seul fichier confirmé)

**État système:** Production-ready à 91.5% → Phase réaliste planifiée
**Fichiers CLAUDE_MASTER dans projet:** 1 seul (✅ règle respectée)

### 🖥️ SESSION Claude Desktop - [DATE À COMPLÉTER]
**Travail effectué par Claude Desktop:**
- [À DOCUMENTER lors prochaine utilisation Claude Desktop]

### 🖥️ SESSION Claude Desktop - [DATE À COMPLÉTER] 
**Travail effectué par Claude Desktop:**
- [À DOCUMENTER lors prochaine utilisation Claude Desktop]

---

## 🛠️ TRAVAIL EFFECTUÉ SESSIONS PRÉCÉDENTES

### 1. 🔍 Recherche des clés API
```bash
# Zones explorées :
- C:\Users\fvegi complet (AppData, Documents, Downloads, Desktop)
- Projet Highlight recherché (non trouvé)
- Tous les .env, .json, .txt, .config
- Historiques bash/PowerShell
- Bases SQLite, cookies navigateurs
- VSCode settings, temp files
```

### 2. 🔐 Google Session Manager (Style Claude Code)
```bash
# Fichiers créés :
- google_session_manager.py      # Gestionnaire cookies session
- setup_google_session.py        # Configuration interactive
- google_pgi_integration.py      # Intégration Drive/Gmail
- google_session_launcher.sh     # Menu interactif
- GOOGLE_SESSION_GUIDE.md       # Documentation
```

### 3. 🤖 Gemini Integration (GRATUIT)
```bash
# Fichiers créés :
- gemini_manager.py              # Gestionnaire principal
- gemini_pgi_integration.py      # Spécialisé électricité
- setup_gemini.sh               # Installation auto
- gemini_integration_launcher.sh # Menu interactif
- GEMINI_GUIDE.md               # Documentation
- config/agents_with_gemini.yaml # Config multi-agents
```

### 4. 🐳 Docker Architecture (Optionnel)
```bash
# Structure complète créée :
- docker-compose.yml            # Multi-services production
- docker-compose.dev.yml        # Dev avec hot-reload
- docker-deploy.sh              # Script déploiement
- Makefile                      # Commandes simplifiées
- DOCKER_GUIDE.md              # Documentation
- docker/
  ├── backend.Dockerfile        # Flask principal
  ├── gemini.Dockerfile         # Service Gemini
  ├── deepseek.Dockerfile       # Service DeepSeek
  ├── ocr.Dockerfile           # Service OCR
  └── nginx.conf               # Reverse proxy
```

### 5. 📚 Documentation créée
```bash
- DOCKER_VS_GITHUB.md          # Explication différences
- docker_vs_github_visual.html  # Version visuelle
- IA_COMPARISON_GUIDE.md       # Comparaison objective IAs
- setup_env.sh                 # Chargement variables env
- .env                         # Fichier config (DeepSeek only)
```

---

## 🚀 COMMANDES ESSENTIELLES

### Démarrage basique
```bash
cd /home/fvegi/dev/pgi-ia
source venv_pgi_ia/bin/activate
source setup_env.sh
python backend/main.py
```

### Vérification système
```bash
python verify_complete_system.py
```

### Gemini (à configurer)
```bash
./setup_gemini.sh
# Obtenir clé sur https://makersuite.google.com/app/apikey
./gemini_integration_launcher.sh
```

### Google Session (optionnel)
```bash
./google_session_launcher.sh
# Option 1 : Configurer cookies
```

### Docker (optionnel)
```bash
./docker-deploy.sh
# ou
make up
```

---

## 📋 TODO - À POURSUIVRE

### 1. Configuration Gemini
- [ ] Obtenir clé API gratuite
- [ ] Tester analyse PDF
- [ ] Intégrer dans backend Flask

### 2. Finalisation système
- [ ] Démarrer backend Flask
- [ ] Tester interface complète
- [ ] Uploader plans PDF test

### 3. Optimisations
- [ ] Configurer Redis cache
- [ ] Setup PostgreSQL (optionnel)
- [ ] Monitoring services

---

## 🎯 CONTEXTE POUR NOUVEAU CHAT

### Message d'ouverture recommandé :
```
Je continue le travail sur PGI-IA v4.1. 
Référence : CLAUDE_MASTER_REFERENCE.md dans /home/fvegi/dev/pgi-ia

État actuel :
- DeepSeek configuré ✅
- Gemini prêt mais pas de clé
- Google Session manager créé
- Docker architecture prête
- Backend Flask prêt à démarrer

Prochaine étape : [CE QUE TU VEUX FAIRE]
```

### Fichiers clés à mentionner :
1. **CLAUDE_MASTER_REFERENCE.md** (ce fichier)
2. **CLAUDE.md** - Config générale projet
3. **verify_complete_system.py** - État système
4. **gemini_integration_launcher.sh** - Menu Gemini
5. **google_session_launcher.sh** - Menu Google

### APIs disponibles :
- DeepSeek : sk-ccc37a109afb461989af8cf994a8bc60
- Gemini : À configurer
- OpenAI : Non trouvée
- Anthropic : Non trouvée

---

## 💡 ARCHITECTURE ACTUELLE

```
pgi-ia/
├── backend/                    # Flask API
├── frontend/                   # Interface Tailwind
├── config/                     # Configurations
├── plans_kahnawake/           # PDFs projet 1
├── plans_alexis_nihon/        # PDFs projet 2
├── docker/                    # Dockerfiles
├── venv_pgi_ia/              # Environnement Python
├── *.py                      # Scripts principaux
├── *.sh                      # Scripts bash
├── *.md                      # Documentation
└── .env                      # Variables environnement
```

---

## 🔧 DÉCISIONS TECHNIQUES

1. **Rester en local** pour développement (pas Docker)
2. **Utiliser DeepSeek** comme API principale
3. **Ajouter Gemini** pour analyse PDF (gratuit)
4. **Google Session** pour accès Drive (optionnel)
5. **GitHub** pour versioning (déjà fait)
6. **Docker** prêt pour production future

---

## 📞 POINTS DE CONTACT

- GitHub : https://github.com/fvegiard/pgi-ia
- Local : /home/fvegi/dev/pgi-ia
- Windows : C:\Users\fvegi\dev\pgi-ia
- Backend : http://localhost:5000
- Frontend : file:///C:/Users/fvegi/dev/pgi-ia/frontend/index.html

---

## 🎯 RÉSUMÉ EXÉCUTIF

**Projet** : PGI-IA v4.1 - Gestion électrique industrielle avec IA
**État** : 88.9% fonctionnel, manque config Gemini
**APIs** : DeepSeek OK, autres non trouvées
**Nouveau** : Google Session + Gemini + Docker créés
**Prochain** : Configurer Gemini et démarrer système

---

*Ce document contient TOUT le contexte nécessaire pour continuer dans un nouveau chat*
