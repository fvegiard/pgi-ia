# Makefile pour PGI-IA Docker
.PHONY: help build up down logs shell clean test deploy

# Variables
COMPOSE = docker compose
BACKEND = pgi-ia-backend
GEMINI = pgi-ia-gemini

# Aide par défaut
help:
	@echo "🐳 PGI-IA Docker Commands"
	@echo "========================"
	@echo "make build    - Build tous les conteneurs"
	@echo "make up       - Démarrer tous les services"
	@echo "make down     - Arrêter tous les services"
	@echo "make logs     - Voir les logs"
	@echo "make shell    - Entrer dans le backend"
	@echo "make clean    - Nettoyer tout"
	@echo "make test     - Lancer les tests"
	@echo "make deploy   - Déployer en production"

# Build
build:
	$(COMPOSE) build

# Démarrer
up:
	$(COMPOSE) up -d
	@echo "✅ Services démarrés :"
	@echo "   Frontend : http://localhost"
	@echo "   Backend  : http://localhost:5000"
	@echo "   Gemini   : http://localhost:5001"

# Arrêter
down:
	$(COMPOSE) down

# Logs
logs:
	$(COMPOSE) logs -f

# Shell backend
shell:
	docker exec -it $(BACKEND) bash

# Shell Gemini
shell-gemini:
	docker exec -it $(GEMINI) bash

# Clean
clean:
	$(COMPOSE) down -v --remove-orphans
	docker system prune -f

# Tests
test:
	docker exec $(BACKEND) python -m pytest

# Deploy production
deploy:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

# Dev mode
dev:
	$(COMPOSE) up

# Restart service
restart-%:
	$(COMPOSE) restart $*

# Backup DB
backup:
	docker exec pgi-ia-postgres pg_dump -U pgiia pgiia > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Status
status:
	docker ps --filter "name=pgi-ia"
