# 🐳 Guide Docker pour PGI-IA

## 🎯 Pourquoi Docker ?

### Avantages
- ✅ **Isolation** : Chaque service dans son conteneur
- ✅ **Reproductibilité** : Fonctionne pareil partout
- ✅ **Scalabilité** : Facile d'ajouter des instances
- ✅ **Microservices** : Séparation des responsabilités
- ✅ **CI/CD Ready** : Déploiement automatisé

### Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│    Nginx    │────▶│   Backend   │
│  (Static)   │     │  (Reverse   │     │   (Flask)   │
└─────────────┘     │   Proxy)    │     └──────┬──────┘
                    └──────┬──────┘             │
                           │                    ▼
┌─────────────┐           │            ┌─────────────┐
│   Gemini    │◀──────────┴───────────▶│    Redis    │
│  Service    │                         │   (Cache)   │
└─────────────┘                         └─────────────┘
                                               │
┌─────────────┐     ┌─────────────┐           ▼
│  DeepSeek   │     │     OCR     │    ┌─────────────┐
│  Service    │     │   Service   │    │  PostgreSQL │
└─────────────┘     └─────────────┘    │     (DB)    │
                                       └─────────────┘
```

## 🚀 Démarrage Rapide

### 1. Installation basique
```bash
# Clone et configure
cd /home/fvegi/dev/pgi-ia
./docker-deploy.sh

# Choix 2 : Build
# Puis choix 1 : Démarrer
```

### 2. Avec GPU (recommandé)
```bash
# Installer nvidia-docker d'abord
./docker-deploy.sh
# Choix 7 et suivre les instructions

# Puis démarrer avec GPU
docker compose up -d
```

## 📋 Services Disponibles

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Frontend | 80 | http://localhost | Interface web |
| Backend | 5000 | http://localhost:5000 | API principale |
| Gemini | 5001 | http://localhost:5001 | Analyse PDF |
| DeepSeek | 5002 | http://localhost:5002 | IA orchestration |
| OCR | 5003 | http://localhost:5003 | Extraction texte |
| PostgreSQL | 5432 | - | Base de données |
| Redis | 6379 | - | Cache |

## 🛠️ Commandes Utiles

### Gestion des conteneurs
```bash
# Voir tous les conteneurs
docker ps

# Logs d'un service spécifique
docker logs pgi-ia-backend -f
docker logs pgi-ia-gemini -f

# Entrer dans un conteneur
docker exec -it pgi-ia-backend bash

# Redémarrer un service
docker compose restart backend
```

### Développement
```bash
# Mode dev avec hot-reload
docker compose -f docker-compose.dev.yml up

# Rebuild après changements
docker compose build backend
docker compose up -d backend

# Voir les ressources utilisées
docker stats
```

### Maintenance
```bash
# Backup base de données
docker exec pgi-ia-postgres pg_dump -U pgiia pgiia > backup.sql

# Restore
docker exec -i pgi-ia-postgres psql -U pgiia pgiia < backup.sql

# Nettoyer les images/volumes non utilisés
docker system prune -a
```

## 🔧 Configuration

### Variables d'environnement (.env)
```env
# APIs
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Database
POSTGRES_USER=pgiia
POSTGRES_PASSWORD=pgiia_secure_password
POSTGRES_DB=pgiia

# Redis
REDIS_PASSWORD=redis_secure_password
```

### Volumes persistants
- `postgres_data` : Données PostgreSQL
- `./plans_*` : Plans PDF
- `./models` : Modèles IA
- `./downloads` : Fichiers téléchargés

## 🚨 Dépannage

### "Cannot connect to Docker daemon"
```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
# Logout/login
```

### "GPU not available"
```bash
# Vérifier nvidia-docker
docker run --rm --gpus all nvidia/cuda:11.7.0-base-ubuntu20.04 nvidia-smi
```

### "Port already in use"
```bash
# Trouver et tuer le process
sudo lsof -i :5000
sudo kill -9 <PID>
```

### "Out of memory"
```bash
# Augmenter les limites Docker
# Éditer ~/.docker/daemon.json
{
  "memory": 8192,
  "memory-swap": 16384
}
```

## 🔄 Workflow de Développement

1. **Développement local** (actuel)
   - Rapide pour tests
   - Accès direct aux fichiers
   - Debug facile

2. **Docker pour staging**
   - Test d'intégration
   - Validation architecture
   - Tests de charge

3. **Docker pour production**
   - Déploiement cloud
   - Orchestration K8s
   - Monitoring

## 🎯 Comparaison

| Aspect | Local (venv) | Docker |
|--------|--------------|--------|
| **Setup** | Simple | Plus complexe |
| **Isolation** | Partielle | Totale |
| **Reproductibilité** | Moyenne | Excellente |
| **Performance** | Native | -5% overhead |
| **GPU** | Direct | nvidia-docker |
| **Debug** | Facile | Plus difficile |
| **Déploiement** | Manuel | Automatique |

## 📊 Recommandation

### Utilise Docker si :
- ✅ Déploiement production
- ✅ Équipe multiple
- ✅ CI/CD nécessaire
- ✅ Microservices

### Reste en local si :
- ✅ Développement actif
- ✅ Prototypage rapide
- ✅ Debug fréquent
- ✅ Projet personnel

---
*Docker est optionnel mais recommandé pour la production !*
