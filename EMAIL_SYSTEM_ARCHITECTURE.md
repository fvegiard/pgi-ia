# 📧 Architecture Système Email Intelligent PGI-IA

## 🎯 Vision Globale
Le système email transforme PGI-IA en assistant autonome qui surveille, trie et traite automatiquement tous les emails liés aux projets électriques.

## 🔄 Flux Complet Email → IA → Action

### 1. **Capture Emails (Outlook → PGI-IA)**
```
Outlook/Exchange → Email Watcher Service → PGI-IA API → Processing Queue
```

**Technologies:**
- **Option A**: Graph API Microsoft (OAuth2)
- **Option B**: IMAP/Exchange Web Services
- **Fréquence**: Push en temps réel ou polling toutes les 60s

**Service `email_watcher.py`:**
```python
# Surveille la boîte Outlook
# Filtre emails pertinents (domaines clients, mots-clés)
# Pousse vers PGI-IA avec métadonnées
```

### 2. **Réception & Classification Intelligente**

**Pipeline de traitement:**
1. **Email arrive** → Queue de traitement
2. **IA Classificateur** analyse:
   - Sujet
   - Expéditeur (domaine, historique)
   - Corps du message
   - Pièces jointes
   - Mots-clés projet

3. **Classification automatique:**
   ```
   Email → IA → {
     "project": "S-1086" ou "C-24-048",
     "type": "directive" | "plan" | "changement" | "question",
     "priority": "urgent" | "normal" | "bas",
     "confidence": 0.95
   }
   ```

### 3. **Actions Automatiques par Type**

#### 📋 **DIRECTIVE**
- Extraction automatique des infos
- Création entrée tableau directives
- Calcul impact financier
- Notification équipe

#### 📐 **PLAN/DESSIN**
- Détection PDF/DWG en pièce jointe
- OCR automatique (EasyOCR)
- Extraction métadonnées
- Indexation base de données
- Analyse différences si révision

#### 🔄 **CHANGEMENT**
- Parse demande de changement
- Évaluation impact (coût/délai)
- Création tâche automatique
- Flag pour approbation

#### ❓ **QUESTION/AUTRE**
- Tag pour réponse manuelle
- Suggestion réponses basées sur historique
- Routage vers bon expert

### 4. **Interface Utilisateur**

**Dashboard principal:**
- Badge emails non lus sur sidebar
- Timeline temps réel des emails entrants

**Onglet Emails dédié:**
```
┌─────────────────────────────────────────┐
│ 📧 Emails         [3 non lus]           │
├─────────────────────────────────────────┤
│ Filtres: [Tous] [Kahnawake] [Alexis]   │
│         [Directives] [Plans] [Questions]│
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ ⚡ Directive CD-203 - Kahnawake     │ │
│ │ De: architecte@xyz.com              │ │
│ │ Il y a 5 min - Auto-classé          │ │
│ │ [Voir] [Traiter] [Assigner]         │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ 📐 Rev.3 Plan E-101 - Alexis-Nihon │ │
│ │ De: ing@abc.com                     │ │
│ │ Il y a 23 min - PDF détecté         │ │
│ │ [Analyser] [Comparer Rev.2]         │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 🛠️ Architecture Technique

### Backend Components

1. **`email_watcher_service.py`**
   - Service Windows/Linux
   - Connexion Outlook/Exchange
   - Push vers API PGI-IA

2. **`backend/email_processor.py`**
   - Réception emails
   - Queue de traitement
   - Orchestration IA

3. **`backend/email_classifier_ai.py`**
   - Modèle DeepSeek fine-tuné
   - Classification multi-label
   - Extraction entités

4. **`backend/email_actions.py`**
   - Actions automatiques
   - Intégration avec modules existants
   - Notifications

### Frontend Components

1. **Dashboard Update**
   - Nouveau `EmailsView` component
   - Badge temps réel (WebSocket)
   - Integration timeline

2. **Email Management UI**
   - Liste emails avec filtres
   - Actions rapides
   - Détails avec preview

### Base de données

```sql
-- Nouvelle table emails
CREATE TABLE emails (
    id UUID PRIMARY KEY,
    subject TEXT,
    from_address TEXT,
    to_address TEXT,
    body TEXT,
    received_at TIMESTAMP,
    project_id VARCHAR(20),
    type VARCHAR(50),
    status VARCHAR(20),
    confidence FLOAT,
    processed_at TIMESTAMP,
    actions_taken JSONB
);

-- Table pièces jointes
CREATE TABLE email_attachments (
    id UUID PRIMARY KEY,
    email_id UUID REFERENCES emails(id),
    filename TEXT,
    file_type VARCHAR(20),
    file_path TEXT,
    processed BOOLEAN
);
```

## 🔐 Sécurité & Configuration

### Variables d'environnement
```bash
# Email Configuration
OUTLOOK_CLIENT_ID=xxx
OUTLOOK_CLIENT_SECRET=xxx
OUTLOOK_TENANT_ID=xxx
EMAIL_POLL_INTERVAL=60
EMAIL_FILTER_DOMAINS=kahnawake.com,alexisnihon.ca,drelectrique.com

# IA Configuration
EMAIL_CLASSIFIER_MODEL=deepseek-email-v1
EMAIL_CONFIDENCE_THRESHOLD=0.8
AUTO_PROCESS_THRESHOLD=0.95
```

### Permissions
- Read emails (Mail.Read)
- Mark as read (Mail.ReadWrite)
- Access attachments
- Move to folders

## 📊 Métriques & Monitoring

### KPIs suivis:
- Emails traités/jour
- Précision classification
- Temps moyen traitement
- Actions automatiques réussies
- Économie temps (heures/semaine)

### Logs détaillés:
```
[2025-07-11 09:15:23] Email reçu: "RE: Directive CD-203" 
[2025-07-11 09:15:24] Classification: Kahnawake/Directive (95% confiance)
[2025-07-11 09:15:25] Action: Création directive automatique
[2025-07-11 09:15:26] Notification: Équipe Kahnawake alertée
```

## 🚀 Roadmap Implementation

### Phase 1: MVP (1 semaine)
- [x] Documentation architecture
- [ ] Interface emails basique
- [ ] Service email simple (IMAP)
- [ ] Classification manuelle

### Phase 2: IA Integration (2 semaines)
- [ ] Classifier IA DeepSeek
- [ ] Actions automatiques directives
- [ ] Detection plans PDF
- [ ] Timeline integration

### Phase 3: Production (1 semaine)
- [ ] OAuth2 Microsoft
- [ ] Service Windows robuste
- [ ] Monitoring complet
- [ ] Tests end-to-end

## 🔧 Commandes Développement

```bash
# Démarrer service email
python email_watcher_service.py

# Tester classification
python test_email_classifier.py --email "test.eml"

# Fine-tuner modèle
python train_email_classifier.py --dataset emails_labeled.json

# Monitor en temps réel
python monitor_emails.py --live
```

## 📝 Notes Importantes

1. **Priorité**: Les directives sont TOUJOURS prioritaires
2. **Seuil**: Auto-traitement seulement si confiance > 95%
3. **Backup**: Tous les emails sont archivés avant traitement
4. **Rollback**: Possibilité d'annuler actions automatiques sous 24h
5. **GDPR**: Respect vie privée, pas de lecture emails personnels

---
*Ce document est LA référence pour le système email PGI-IA. À mettre à jour à chaque évolution.*