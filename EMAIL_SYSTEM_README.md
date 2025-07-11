# 📧 Système Email Intelligent PGI-IA - Guide Rapide

## 🚀 Démarrage Rapide

### 1. Configuration initiale
```bash
# Configurer les credentials Outlook
export OUTLOOK_CLIENT_ID="votre-client-id"
export OUTLOOK_CLIENT_SECRET="votre-secret"
export OUTLOOK_TENANT_ID="votre-tenant-id"

# Ou utiliser le script de configuration
./setup_email_service.sh
```

### 2. Démarrer le service email
```bash
# Service principal
python email_watcher_service.py

# Ou en mode daemon
python email_watcher_service.py --daemon
```

### 3. Vérifier le dashboard
- Ouvrir PGI-IA Dashboard
- Cliquer sur l'onglet "Emails" 📧
- Les emails arrivent en temps réel

## 📊 Workflow Email → Action

```
Email reçu → Classification IA → Action automatique
     ↓              ↓                    ↓
  Outlook      Projet détecté      Selon le type:
              (95% confiance)       - Directive → Tableau
                                   - Plan → OCR + Index
                                   - Question → Flag
```

## 🎯 Cas d'Usage

### Directive par email
1. **Email reçu**: "Directive CD-203 pour Kahnawake"
2. **IA détecte**: Type=Directive, Projet=S-1086
3. **Action**: Création automatique dans tableau directives
4. **Notification**: Timeline + Badge email

### Plan révisé
1. **Email reçu**: "Rev.3 du plan E-101" + PDF attaché
2. **IA détecte**: Type=Plan, Projet=Alexis-Nihon
3. **Action**: OCR → Comparaison Rev.2 → Alerte changements
4. **Notification**: Différences surlignées

## ⚙️ Configuration Avancée

### Filtres emails
```python
# config/email_filters.py
ALLOWED_DOMAINS = [
    "kahnawake.com",
    "alexisnihon.ca",
    "drelectrique.com"
]

KEYWORDS_TRIGGER = [
    "directive", "plan", "révision",
    "changement", "modification"
]
```

### Seuils IA
```python
# config/ai_thresholds.py
AUTO_PROCESS_CONFIDENCE = 0.95  # Process automatique
MANUAL_REVIEW_CONFIDENCE = 0.80  # Revue manuelle
REJECT_CONFIDENCE = 0.50  # Rejet automatique
```

## 🔍 Monitoring

### Logs temps réel
```bash
# Voir tous les emails traités
tail -f logs/email_processor.log

# Filtrer par projet
grep "Kahnawake" logs/email_processor.log

# Statistiques du jour
python email_stats.py --today
```

### Métriques Dashboard
- Emails traités: Compteur temps réel
- Classification accuracy: % de précision
- Actions automatiques: Succès/Échecs
- Temps économisé: Heures/semaine

## 🚨 Troubleshooting

### Email non classé
1. Vérifier confiance IA (doit être > 80%)
2. Ajouter domaine expéditeur aux filtres
3. Enrichir dataset entraînement

### Service ne démarre pas
```bash
# Vérifier credentials
python test_outlook_connection.py

# Vérifier permissions
python check_email_permissions.py
```

### Actions échouent
- Vérifier connexion backend Flask
- Valider format des directives
- Logs: `logs/email_actions_errors.log`

## 📈 Roadmap

- [x] Architecture documentée
- [ ] Interface emails dans dashboard
- [ ] Service capture Outlook
- [ ] IA classification DeepSeek
- [ ] Actions automatiques
- [ ] Tests end-to-end
- [ ] Déploiement production

---
*Pour plus de détails techniques, voir [EMAIL_SYSTEM_ARCHITECTURE.md](./EMAIL_SYSTEM_ARCHITECTURE.md)*