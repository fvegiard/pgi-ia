# 📋 INVENTAIRE SYSTÈME PGI-IA - NE JAMAIS RECRÉER
# Dernière mise à jour: 11/07/2025 13:55

## 🚨 RÈGLE ABSOLUE: TOUJOURS VÉRIFIER AVANT DE CRÉER

## ✅ FICHIERS EXISTANTS - NE PAS RECRÉER

### 🎨 FRONTEND (Interface)
- **dashboard.html** (38KB) - Dashboard moderne complet avec sidebar
- **dashboard.js** (10KB) - Logique avec Chart.js (bug resize CORRIGÉ)
- **index.html** (24KB) - Interface originale
- **script.js** (17KB) - JavaScript original
- **style.css** (7KB) - Styles CSS

### 🔧 BACKEND (API)
- **main.py** - Serveur Flask principal (avec email_bp, notes_bp, photos_bp)
- **database_manager.py** - Gestionnaire DB centralisé ✅
- **email_classifier_deepseek.py** - Classification emails ✅
- **email_endpoints.py** - API endpoints emails ✅
- **notes_system.py** - Système notes intelligentes ✅
- **notes_endpoints.py** - API endpoints notes ✅
- **photo_gps_system.py** - Système photos GPS ✅
- **photo_endpoints.py** - API endpoints photos ✅

### 📊 BASE DE DONNÉES
- **database_schema_extended.sql** - Schéma complet 8 tables ✅
- **pgi_ia.db** - Base SQLite (si existe)

### 📝 DOCUMENTATION
- **CLAUDE_MASTER_REFERENCE.md** - FICHIER UNIQUE DE RÉFÉRENCE
- **CLAUDE.md** - Config projet
- **README.md** - Documentation principale
- Nombreux autres .md (voir liste)

## 🛡️ WORKFLOW ANTI-DUPLICATION

### AVANT TOUTE CRÉATION:
1. **VÉRIFIER** si fichier existe: `ls -la | grep [nom]`
2. **LIRE** le fichier existant: `Read tool`
3. **MODIFIER** au lieu de recréer: `Edit tool`
4. **ENRICHIR** au lieu de remplacer

### COMMANDES VÉRIFICATION:
```bash
# Vérifier frontend
ls -la frontend/

# Vérifier backend
ls -la backend/

# Vérifier racine
ls -la *.md *.py *.sql

# Rechercher fichier
find . -name "*dashboard*" -type f
find . -name "*notes*" -type f
```

## 🎯 MODULES DASHBOARD EXISTANTS

### ✅ DÉJÀ IMPLÉMENTÉS:
- Sidebar navigation complète
- Onglet Emails avec badge rouge
- Graphiques Chart.js
- Tableau de bord principal
- Système de tabs

### 🆕 À AJOUTER (PAS RECRÉER):
- Module Notes dans dashboard existant
- Module Photos dans dashboard existant
- Module Plan Principal
- Module Réunions
- Vue 3D

## ⚠️ ERREURS À ÉVITER
1. ❌ Créer nouveau dashboard.html
2. ❌ Créer nouveau système notes
3. ❌ Recréer base données
4. ❌ Dupliquer endpoints existants
5. ❌ Ignorer fichiers existants

## 🔍 RÉFLEXE OBLIGATOIRE
**TOUJOURS faire `ls -la` AVANT `Write`**