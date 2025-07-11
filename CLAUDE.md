# Configuration Claude Code pour PGI-IA

## 🔗 Guides associés
- **Claude Desktop**: Voir [CLAUDE_DESKTOP_SETUP.md](./CLAUDE_DESKTOP_SETUP.md) pour utilisation dans Claude Desktop
- **Mission accomplie**: Voir [MISSION_ACCOMPLIE.md](./MISSION_ACCOMPLIE.md) pour le résumé complet du projet

## Environnement de développement
- **Projet**: PGI-IA (Progiciel de Gestion Intégré assisté par Intelligence Artificielle)
- **Langage principal**: Python 3.12+
- **Framework web**: Flask
- **Framework ML/AI**: PyTorch, Transformers, PEFT
- **Environnement virtuel**: `/home/fvegi/dev/pgi-ia/venv_pgi_ia/`

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

### Entraînement DeepSeek
```bash
/home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python /home/fvegi/dev/pgi-ia/deepseek_finetune_english_complete.py
```

### Audits
```bash
# Audit technique DeepSeek
/home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python /home/fvegi/dev/pgi-ia/audit_deepseek.py

# Audit UX Justina  
/home/fvegi/dev/pgi-ia/venv_pgi_ia/bin/python /home/fvegi/dev/pgi-ia/audit_justina.py
```

## Structure du projet
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
│   └── agents.yaml          # Config multi-agents
├── plans_kahnawake/         # Plans PDF Kahnawake (300+)
├── plans_alexis_nihon/      # Plans PDF Alexis-Nihon
├── venv_pgi_ia/            # Environnement virtuel
└── deepseek_training_complete/ # Modèles entraînés
```

## APIs configurées
- **DeepSeek API**: ✅ Configurée et fonctionnelle
- **OpenAI API**: ✅ Configurée 
- **Anthropic API**: ⚠️ Non configurée
- **Google API**: ⚠️ Non configurée

## Variables d'environnement
```bash
export OPENAI_API_KEY="sk-..."
export DEEPSEEK_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."  # Optionnel
export GOOGLE_API_KEY="..."        # Optionnel
```

## Statut système
- **GPU**: ✅ NVIDIA GeForce RTX 4060 détectée
- **Mémoire**: ✅ 11.7 GB disponible
- **Backend Flask**: ✅ Port 5000 actif
- **Dépendances**: ✅ 91.5% installées et fonctionnelles

## Projets gérés
1. **S-1086 - Musée Kahnawake**: Estimation (8 directives)
2. **C-24-048 - Place Alexis-Nihon**: Construction (6 directives)

## Fonctionnalités
- ✅ Timeline temps réel
- ✅ Drag-drop upload de plans PDF
- ✅ OCR automatique avec EasyOCR
- ✅ Calculs financiers automatiques
- ✅ Interface responsive Tailwind CSS
- ✅ Multi-agents IA (OpenAI, DeepSeek, Claude, Gemini)
- ✅ Fine-tuning DeepSeek local
- ✅ Audits automatisés (DeepSeek + Justina)

## Workflow de développement
1. Activation environnement
2. Démarrage backend Flask
3. Ouverture frontend dans navigateur
4. Tests et audits réguliers
5. Entraînement modèles selon besoins

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

### Fichiers de configuration
- `CLAUDE.md` - Configuration générale (ce fichier)
- `CLAUDE_DESKTOP_SETUP.md` - Guide spécifique Claude Desktop
- `README.md` - Documentation projet
- `.gitignore` - Fichiers ignorés par Git

## Commandes git
```bash
git add .
git commit -m "Description des changements"
git push origin main  # Nécessite authentification manuelle
```

## Support et troubleshooting
- **Logs système**: `/home/fvegi/dev/pgi-ia/system_verification.log`
- **Logs entraînement**: `/home/fvegi/dev/pgi-ia/deepseek_finetune_complete.log`
- **Rapports d'audit**: `/home/fvegi/dev/pgi-ia/system_verification_report.json`

---
*Configuration mise à jour automatiquement par Claude Code*