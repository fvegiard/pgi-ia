# 📧 Dashboard PGI-IA avec Module Emails

## 🎉 Nouvelle Interface Moderne

### Fichiers créés
- `frontend/dashboard.html` - Interface moderne complète avec emails
- `frontend/dashboard.js` - Logique JavaScript
- `start_dashboard.sh` - Script de lancement

### 🚀 Lancement rapide
```bash
cd /home/fvegi/dev/pgi-ia
./start_dashboard.sh
# Ouvrir http://localhost:8080/dashboard.html
```

## 📋 Fonctionnalités Emails

### Interface
- **Badge rouge** : Compteur emails non lus (3 par défaut)
- **Filtres** : Par type (Directive, Plan, Question), par projet
- **Recherche** : Barre de recherche intégrée
- **Stats** : 4 cartes avec métriques emails

### Types d'emails
1. **Directives** (⚡) - Priorité haute, bordure rouge
2. **Plans** (📐) - Pièces jointes, analyse IA
3. **Questions** (❓) - Réponses suggérées
4. **Confirmations** - Auto-classées

### Actions automatiques
- **Traiter automatiquement** : Création directive auto
- **Analyser avec IA** : OCR et extraction données
- **Suggérer réponse** : Réponses pré-rédigées

### Panel IA
- Classification automatique (95% précision)
- Règles actives configurables
- Métriques de performance
- Actions rapides

## 🎨 Design

### Thème clair moderne
- Fond gris clair (#F3F4F6)
- Cartes blanches avec ombres
- Accents bleus (#3B82F6)
- Icônes Lucide

### Responsive
- Sidebar collapsible
- Grilles adaptatives
- Tables scrollables
- Mobile-friendly

## 🔧 Architecture

### Technologies
- **HTML5** + Tailwind CSS (CDN)
- **JavaScript** vanilla (pas de build)
- **Lucide Icons** pour les icônes
- **Chart.js** pour les graphiques

### Structure
```
frontend/
├── dashboard.html    # Nouvelle interface
├── dashboard.js      # Logique
├── index.html       # Ancienne interface (dark)
├── script.js        # Ancien JS
└── style.css        # Ancien CSS
```

## 📊 Données mockées

### Emails de démo
- 3 non lus (directive, plan, question)
- 1 traité (confirmation)
- Projets : Kahnawake (S-1086), Alexis-Nihon (C-24-048)

### Statistiques
- Total : 127 emails
- Non lus : 3
- Traités aujourd'hui : 12
- En attente : 5

## 🚦 Prochaines étapes

### Backend
1. Créer endpoints `/api/emails/*`
2. Intégrer email_processor.py
3. Connecter à Outlook/IMAP

### Frontend
1. Connexion API réelle
2. WebSocket pour temps réel
3. Détails email (modal/panel)
4. Composer email

### IA
1. Classifier DeepSeek
2. Actions automatiques
3. Apprentissage continu

## 🐛 Debug

Si problème :
```bash
# Vérifier le port
lsof -i :8080

# Tuer le process
kill -9 [PID]

# Relancer
./start_dashboard.sh
```

---
*Dashboard créé le 11/07/2025 - Ne pas oublier de commiter !*