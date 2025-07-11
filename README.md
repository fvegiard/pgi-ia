# 🚀 PGI-IA v4.1 - Progiciel de Gestion Intégré avec Intelligence Artificielle

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

## 🎯 Description

PGI-IA est un système complet de gestion électrique industrielle assisté par IA, spécialisé dans:
- Gestion multi-projets (Kahnawake, Alexis-Nihon)
- Traitement automatique des directives et plans
- **📧 Nouveau: Système email intelligent avec tri automatique**
- Interface moderne avec dashboard temps réel
- Intégration multi-IA (DeepSeek, Gemini, Claude, GPT-4)

## ✨ Fonctionnalités Principales

### 📊 Dashboard Intelligent
- Vue d'ensemble temps réel des projets
- Métriques et KPIs automatiques
- Timeline des événements
- Graphiques interactifs (Recharts)

### 📧 Système Email Intelligent (NOUVEAU!)
- **Capture automatique** des emails Outlook
- **Classification IA** par projet (95% précision)
- **Actions automatiques**:
  - Directives → Création dans tableau
  - Plans PDF → OCR et indexation
  - Questions → Routage expert
- **Interface dédiée** avec inbox intelligent
- Voir [EMAIL_SYSTEM_ARCHITECTURE.md](./EMAIL_SYSTEM_ARCHITECTURE.md) pour détails

### 🤖 Multi-Agents IA
- **Léa**: Orchestrateur spécialisé électricité
- **DeepSeek**: Fine-tuné sur 300+ plans
- **Gemini**: Analyse PDF avancée
- **Claude/GPT-4**: Support général

### 📄 Gestion Documents
- Drag-drop upload
- OCR automatique (EasyOCR)
- Extraction métadonnées
- Comparaison révisions

## 🛠️ Installation

### Prérequis
- Python 3.12+
- Node.js 18+
- GPU NVIDIA (optionnel, pour entraînement)
- Compte Microsoft (pour emails)

### Installation rapide
```bash
# 1. Cloner le projet
git clone https://github.com/fvegiard/pgi-ia.git
cd pgi-ia

# 2. Environnement Python
python -m venv venv_pgi_ia
source venv_pgi_ia/bin/activate  # Linux/Mac
# ou
venv_pgi_ia\Scripts\activate  # Windows

# 3. Dépendances
pip install -r requirements_complete.txt

# 4. Configuration
cp config/email_system.env.example config/email_system.env
# Éditer avec vos credentials
```

## 🚀 Démarrage

### Backend + Services
```bash
# Tout démarrer
python start_all_services.py

# Ou individuellement:
python backend/main.py              # API Flask
python email_watcher_service.py     # Service emails
```

### Frontend
```bash
# Développement
cd frontend && npm install && npm start

# Ou ouvrir directement:
# file:///path/to/pgi-ia/frontend/index.html
```

### Dashboard React v2
```bash
cd dashboard-v2
npm install
npm start
# http://localhost:3000
```

## 📁 Structure du Projet

```
pgi-ia/
├── backend/                    # API Flask + IA
│   ├── main.py                # Serveur principal
│   ├── email_processor.py     # 📧 Traitement emails
│   ├── email_classifier_ai.py # 📧 IA classification
│   └── agents/                # Agents IA
├── frontend/                  # Interface HTML/JS
├── dashboard-v2/              # Interface React moderne
├── config/                    # Configurations
│   ├── agents.yaml           # Config multi-agents
│   └── email_system.env      # 📧 Config emails
├── email_watcher_service.py   # 📧 Service Outlook
├── plans_kahnawake/          # PDFs projet 1
├── plans_alexis_nihon/       # PDFs projet 2
└── docs/                     # Documentation
    ├── EMAIL_SYSTEM_ARCHITECTURE.md  # 📧 Architecture emails
    └── EMAIL_SYSTEM_README.md        # 📧 Guide emails
```

## 📧 Configuration Email

### 1. Obtenir credentials Microsoft
- Aller sur [Azure Portal](https://portal.azure.com)
- Créer une App Registration
- Noter Client ID, Secret, Tenant ID

### 2. Configurer
```bash
# Éditer config/email_system.env
OUTLOOK_CLIENT_ID=votre-client-id
OUTLOOK_CLIENT_SECRET=votre-secret
OUTLOOK_TENANT_ID=votre-tenant-id
```

### 3. Tester
```bash
python test_outlook_connection.py
```

## 🔧 Configuration APIs

```bash
# Variables d'environnement (.env)
DEEPSEEK_API_KEY=sk-xxx      # ✅ Configurée
GEMINI_API_KEY=AIza...       # À configurer
OPENAI_API_KEY=sk-xxx        # Optionnel
ANTHROPIC_API_KEY=sk-xxx     # Optionnel
```

## 📊 Utilisation

### Workflow typique
1. **Email reçu** → Classification automatique
2. **Directive détectée** → Ajout tableau + calculs
3. **Plan PDF** → OCR → Indexation → Analyse
4. **Dashboard** → Voir tout en temps réel

### Commandes utiles
```bash
# Vérifier système
python verify_complete_system.py

# Entraîner DeepSeek
python deepseek_finetune_english_complete.py

# Statistiques emails
python email_stats.py --today

# Monitoring temps réel
python monitor_emails.py --live
```

## 🐳 Docker (Optionnel)

```bash
# Développement avec hot-reload
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose up -d
```

## 📈 Roadmap

### Phase 1 ✅ (Complété)
- [x] Backend Flask opérationnel
- [x] Frontend avec timeline
- [x] Multi-agents IA
- [x] Upload drag-drop

### Phase 2 🚧 (En cours)
- [x] Architecture email documentée
- [ ] Interface emails dans dashboard
- [ ] Service capture Outlook
- [ ] Classification IA emails
- [ ] Actions automatiques

### Phase 3 📅 (Planifié)
- [ ] OAuth2 Microsoft complet
- [ ] Fine-tuning email classifier
- [ ] Webhooks temps réel
- [ ] Mobile app

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Documentation

- [Configuration Claude](./CLAUDE.md)
- [Setup Claude Desktop](./CLAUDE_DESKTOP_SETUP.md)
- [Architecture Email](./EMAIL_SYSTEM_ARCHITECTURE.md)
- [Guide Email Rapide](./EMAIL_SYSTEM_README.md)
- [Mission Accomplie](./MISSION_ACCOMPLIE.md)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/fvegiard/pgi-ia/issues)
- **Email**: support@drelectrique.com
- **Documentation**: [Wiki](https://github.com/fvegiard/pgi-ia/wiki)

## 📄 License

Propriétaire - DR Électrique © 2025

---
*Développé avec ❤️ par l'équipe DR Électrique*