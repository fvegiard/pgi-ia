# 🚀 PGI-IA - Système de Gestion de Projets Électriques Intelligent

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-purple.svg?style=for-the-badge)](https://deepseek.com)

## 🎯 Vue d'ensemble

PGI-IA est un système intelligent de gestion de projets de construction électrique, spécialement conçu pour le marché québécois. Il intègre l'IA DeepSeek pour offrir une assistance avancée dans la gestion des directives, la documentation et le suivi de projets.

### 🌟 Caractéristiques principales

- **Gestion intelligente des projets** : Suivi en temps réel des projets électriques
- **IA DeepSeek intégrée** : Assistance contextuelle pour les normes CCQ et québécoises
- **Support bilingue** : Français et anglais
- **Projets phares** : Kahnawake Centre Culturel, Alexis Nihon Phase 3
- **ROI démontré** : < 2 mois pour entreprises de 100+ employés

## 🛠️ Architecture

```
pgi-ia/
├── backend/          # API Flask Python
├── frontend/         # Interface React
├── scripts/          # Scripts d'automatisation et IA
├── datasets/         # Données d'entraînement DeepSeek
├── docker/           # Configuration Docker
└── docs/            # Documentation
```

## 🚀 Installation rapide

### Prérequis

- Docker & Docker Compose
- Clé API DeepSeek
- 4GB RAM minimum

### Démarrage

```bash
# 1. Cloner le repo
git clone https://github.com/fvegiard/pgi-ia.git
cd pgi-ia

# 2. Configurer l'environnement
cp .env.example .env
# Éditer .env avec votre clé DeepSeek

# 3. Lancer avec Docker
docker-compose up -d

# 4. Vérifier
curl http://localhost:5000/health
```

## 📊 Fonctionnalités

### Gestion de projets
- Suivi multi-projets simultanés
- Import automatique depuis OneDrive
- Gestion des directives de changement (PCE/ODT)
- Documentation photographique intégrée

### Intelligence artificielle
- Réponses contextuelles aux normes québécoises
- Assistance pour facturation territoire autochtone
- Calcul automatique des ratios CCQ
- Génération de rapports professionnels

### Intégrations
- OneDrive pour synchronisation documents
- DeepSeek API pour IA conversationnelle
- Export vers Excel/PDF
- Notifications temps réel (WebSocket à venir)

## 🔧 Configuration

### Variables d'environnement

```env
# API Keys
DEEPSEEK_API_KEY=votre_clé_ici

# Database
DATABASE_URL=sqlite:////app/data/pgi_ia.db

# Flask
FLASK_ENV=production
SECRET_KEY=générer_une_clé_sécurisée
```

### Volumes Docker

- `/app/data` : Base de données SQLite
- `/app/datasets` : Datasets d'entraînement
- `/app/uploads` : Fichiers uploadés

## 📚 Documentation API

### Endpoints principaux

```bash
GET  /api/projects          # Liste des projets
GET  /api/projects/:id      # Détails d'un projet
POST /api/directives        # Créer une directive
GET  /api/dashboard/metrics # Métriques tableau de bord
```

### Exemple d'utilisation

```python
import requests

# Obtenir les projets
response = requests.get('http://localhost:5000/api/projects')
projects = response.json()

# Interroger l'IA
data = {
    'question': 'Ratio compagnon/apprenti pour chantier commercial?',
    'context': 'CCQ Québec'
}
response = requests.post('http://localhost:5000/api/ai/query', json=data)
```

## 🧪 Scripts utiles

### Dashboard système
```bash
python scripts/pgi_ia_dashboard.py
```

### Import de données
```bash
python scripts/pgi_ia_import_priority_fast.py
```

### Validation dataset
```bash
python scripts/deepseek_training_launcher.py
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📈 Performance

- **Temps de réponse API** : < 200ms
- **Latence IA** : < 2s
- **Capacité** : 1000+ requêtes/minute
- **Uptime cible** : 99.9%

## 🔒 Sécurité

- Authentification JWT
- Rate limiting configurable
- Logs d'audit complets
- Disclaimers CNESST pour questions sécurité

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/fvegiard/pgi-ia/issues)
- **Email** : fvegiard@drelectrique.ca
- **Documentation** : [Wiki](https://github.com/fvegiard/pgi-ia/wiki)

## 📄 Licence

Propriétaire - DR Électrique Inc. © 2025

---

**Développé avec ❤️ pour l'industrie électrique québécoise**

*Propulsé par DeepSeek AI et l'expertise de 17 ans de DR Électrique*