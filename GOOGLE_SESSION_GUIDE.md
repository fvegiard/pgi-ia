# 🔐 Guide : Utiliser les Cookies Google dans PGI-IA

## ⚠️ SÉCURITÉ IMPORTANTE
- **NE JAMAIS** commiter les cookies sur GitHub
- **NE JAMAIS** partager le dossier `.google_session/`
- Les cookies = accès complet à ton compte Google

## 🚀 Installation rapide

### 1. Configurer les cookies (2 méthodes)

#### Méthode A : Configuration manuelle (recommandée)
```bash
cd /home/fvegi/dev/pgi-ia
python setup_google_session.py
```

Puis copie les valeurs depuis Chrome :
1. Ouvre Chrome > F12 > Application > Cookies > google.com
2. Copie les valeurs demandées par le script

#### Méthode B : Import direct (si tu connais les valeurs)
```python
# Dans google_session_manager.py
cookies = {
    '__Secure-1PAPISID': 'FGRvnxMWpw_1FDN9/Ar-WWG-JErAwT-gT',
    '__Secure-3PAPISID': 'FGRvnxMWpw_1FDN9/Ar-WWG-JErAwT-gT',
    'SAPISID': 'BlktU4CWmLf4MYVtvc/AIebJkU2UIyJAWg',
    # ... autres cookies
}
manager.set_cookies(cookies)
```

### 2. Tester l'authentification
```bash
python google_session_manager.py
```

### 3. Utiliser dans PGI-IA
```python
from google_pgi_integration import GooglePGIIntegration

# Initialiser
google = GooglePGIIntegration()

# Rechercher des PDFs
pdfs = google.search_drive_for_pdfs("kahnawake")

# Télécharger un fichier
google.download_file(file_id, "plan.pdf")
```

## 📋 Fonctionnalités disponibles

1. **Recherche Google Drive** - PDFs, documents, etc.
2. **Téléchargement de fichiers** - Direct depuis Drive
3. **Recherche Gmail** - Emails avec pièces jointes
4. **API Google complète** - Toutes les APIs Google

## 🔄 Renouvellement des cookies

Les cookies expirent. Pour les renouveler :
1. Reconnecte-toi à Google dans Chrome
2. Relance `setup_google_session.py`

## 🚧 Limitations

- Les cookies peuvent expirer sans prévenir
- Certaines APIs nécessitent des scopes supplémentaires
- Ne fonctionne pas pour les comptes avec 2FA avancée

## 💡 Alternative recommandée

Pour une solution plus stable, utilise une vraie clé API :
1. https://console.cloud.google.com
2. Créer un projet
3. Activer les APIs
4. Générer une clé API

---
*Ce système est inspiré de Claude Code mais adapté pour PGI-IA*
