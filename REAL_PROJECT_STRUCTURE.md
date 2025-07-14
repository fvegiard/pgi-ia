# 🚀 PGI-IA - Structure RÉELLE du projet

## CE QUI EST VRAIMENT NÉCESSAIRE:

### Frontend (pgi-ia-frontend/)
```
pgi-ia-frontend/
├── dashboard.html          # Interface principale
├── dashboard.js           # Logique JavaScript
├── dashboard_real_data.js # Données réelles des projets
├── emails_real_data.js    # Données réelles des emails
├── style.css             # Styles (si tu en as)
├── index.html            # Page d'accueil (optionnel)
└── assets/
    └── plans/            # Images des plans de construction
        ├── EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1_page_1.png
        └── EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1_page_1_web.jpg
```

### Backend (pgi-ia/)
```
pgi-ia/
├── README.md             # Documentation principale
├── requirements.txt      # Dépendances Python
├── .env                  # Configuration locale
├── .env.example         # Exemple de config
├── backend/
│   ├── main.py          # Point d'entrée
│   ├── api/             # Endpoints API
│   ├── models/          # Modèles de données
│   ├── services/        # Logique métier
│   └── utils/           # Utilitaires
└── data/                # Données locales
```

## CE QUE FAIT TON PROJET:

1. **Dashboard de gestion de projets électriques**
   - Suivi des directives de changement
   - Gestion des QRT (Questions/Réponses Techniques)
   - Classification automatique des emails
   - Géolocalisation des photos de chantier
   - Analyses IA pour optimisation

2. **Projets actifs:**
   - S-1086: Centre Culturel Kahnawake
   - C-24-048: Place Alexis-Nihon
   - C-22-011: Parc Aquatique Beloeil
   - E-25-001: Hydro-Québec Roussillon
   - C-24-089: Cégep Montmorency

## POUR DÉMARRER:

1. **Simple (juste le frontend):**
   ```
   Ouvre dashboard.html dans Chrome
   ```

2. **Complet (avec backend Python):**
   ```bash
   cd pgi-ia
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python backend/main.py
   ```

## PROBLÈME AVEC CLAUDE CODE:

Claude Code a créé 72 fichiers dont 90% sont inutiles:
- ❌ 25+ fichiers .md de "documentation"
- ❌ 20+ scripts .sh qui servent à rien
- ❌ Des "audits" et "verifications" partout
- ❌ Multiples Dockerfiles contradictoires

## LA SOLUTION:

1. Lance `BACKUP_FIRST.bat` pour sauvegarder
2. Lance `CLEAN_THIS_SHIT.bat` pour nettoyer
3. Lance `START_PGI_CLEAN.bat` pour démarrer

---
*PS: À 280$/mois, t'as raison d'être en criss. Claude Code devrait créer du code, pas 50 fichiers de documentation!*
