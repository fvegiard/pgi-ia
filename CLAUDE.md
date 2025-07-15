# Configuration Claude Code pour PGI-IA

## 🔗 Guides associés
- **Claude Desktop**: Voir [CLAUDE_DESKTOP_SETUP.md](./CLAUDE_DESKTOP_SETUP.md) pour utilisation dans Claude Desktop
- **Mission accomplie**: Voir [MISSION_ACCOMPLIE.md](./MISSION_ACCOMPLIE.md) pour le résumé complet du projet
- **Session Master**: Voir [CLAUDE_MASTER_REFERENCE.md](./CLAUDE_MASTER_REFERENCE.md) pour l'état actuel complet

## Environnement de développement
- **Projet**: PGI-IA (Progiciel de Gestion Intégré assisté par Intelligence Artificielle)
- **Langage principal**: Python 3.12+
- **Framework web**: Flask
- **Framework ML/AI**: PyTorch, Transformers, PEFT
- **Environnement virtuel**: `/home/fvegi/dev/pgi-ia/venv_pgi_ia/`

## APIs configurées (MIS À JOUR 15/07/2025)
- **DeepSeek API**: ✅ Configurée et fonctionnelle (sk-ccc37a109afb461989af8cf994a8bc60)
- **Autres APIs**: ❌ Supprimées - Focus DeepSeek uniquement

## Configuration simplifiée
- **API unique**: DeepSeek pour analyse et IA
- **Focus**: Performance et stabilité
- **Supprimé**: Intégrations Gemini/Google/OpenAI/Anthropic

### 🐳 Docker Architecture
- `docker-compose.yml` - Production
- `docker-compose.dev.yml` - Développement
- `docker-deploy.sh` - Déploiement
- `Makefile` - Commandes simplifiées
- `docker/` - Dockerfiles pour chaque service

### 📧 Système Email Intelligent (NOUVEAU)
- **Architecture complète**: Voir [EMAIL_SYSTEM_ARCHITECTURE.md](./EMAIL_SYSTEM_ARCHITECTURE.md)
- **Flux**: Outlook → PGI-IA → Tri automatique par projet → Actions IA
- **Components**:
  - `email_watcher_service.py` - Service capture emails Outlook
  - `backend/email_processor.py` - Traitement et classification
  - `backend/email_classifier_ai.py` - IA tri automatique
  - Interface emails dans dashboard v2
- **Features**:
  - Détection automatique directives/plans/changements
  - Classification par projet (Kahnawake/Alexis-Nihon)
  - Actions automatiques selon le type
  - Timeline temps réel des emails

## Commandes fréquentes

### Activation environnement
```bash
source /home/fvegi/dev/pgi-ia/activate_pgi_ia.sh
```

### Démarrage backend
```bash
/home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python /home/fvegi/dev/pgi-ia/backend/main.py
```

### Vérification système
```bash
/home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python /home/fvegi/dev/pgi-ia/verify_complete_system.py
```

### Nouveaux launchers
```bash
# Gemini
./gemini_integration_launcher.sh

# Google Session
./google_session_launcher.sh

# Docker
./docker-deploy.sh
```

## Structure du projet (MISE À JOUR)
```
/home/fvegi/dev/pgi-ia/
├── backend/                    # API Flask
│   ├── main.py                # Serveur principal
│   ├── agents/                # Agents IA
│   └── requirements.txt       # Dépendances
├── frontend/                  # Interface web
│   ├── index.html            # Interface Tailwind CSS
│   ├── script.js             # JavaScript
│   └── style.css             # Styles
├── config/                   # Configuration
│   ├── agents.yaml          # Config multi-agents
│   └── agents_with_gemini.yaml # NOUVEAU: avec Gemini
├── docker/                   # NOUVEAU: Dockerfiles
│   ├── backend.Dockerfile    
│   ├── gemini.Dockerfile     
│   └── ...
├── plans_kahnawake/         # Plans PDF Kahnawake (300+)
├── plans_alexis_nihon/      # Plans PDF Alexis-Nihon
├── venv_pgi_ia/            # Environnement virtuel
├── deepseek_training_complete/ # Modèles entraînés
├── gemini_*.py             # NOUVEAU: Scripts Gemini
├── google_*.py             # NOUVEAU: Scripts Google Session
├── docker-*.yml            # NOUVEAU: Docker configs
└── *.md                    # Documentation étendue
```

## Variables d'environnement
```bash
export DEEPSEEK_API_KEY="sk-ccc37a109afb461989af8cf994a8bc60"
export GEMINI_API_KEY=""        # À configurer
export OPENAI_API_KEY=""        # Non trouvée
export ANTHROPIC_API_KEY=""     # Non trouvée
```

## Statut système (11/07/2025)
- **GPU**: ✅ NVIDIA GeForce RTX 4060 détectée
- **Mémoire**: ✅ 11.7 GB disponible
- **Backend Flask**: ⚠️ Prêt mais non démarré
- **Dépendances**: ✅ 88.9% installées et fonctionnelles
- **APIs**: DeepSeek OK, autres à configurer

## Workflow de développement
1. Activation environnement
2. Chargement variables (.env ou setup_env.sh)
3. Démarrage backend Flask
4. Ouverture frontend dans navigateur
5. Tests avec Gemini pour PDF
6. Utilisation Google Session si besoin Drive

## 🔄 Synchronisation multi-environnements

### WSL ↔ Claude Desktop
```bash
# Dans WSL
cd /home/fvegi/dev/pgi-ia
git pull origin main

# Dans Claude Desktop
cd /mnt/c/Users/fvegi/dev/pgi-ia
git pull origin main
```

## Commandes git
```bash
git add .
git commit -m "Ajout Gemini + Google Session + Docker"
git push origin main  # Nécessite authentification manuelle
```

## Support et troubleshooting
- **Master Reference**: `/home/fvegi/dev/pgi-ia/CLAUDE_MASTER_REFERENCE.md`
- **Logs système**: `/home/fvegi/dev/pgi-ia/system_verification.log`
- **Logs entraînement**: `/home/fvegi/dev/pgi-ia/deepseek_finetune_complete.log`
- **Rapports d'audit**: `/home/fvegi/dev/pgi-ia/system_verification_report.json`

---
*Configuration mise à jour le 11/07/2025 - Session ajout Gemini/Google/Docker*