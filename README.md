# PGI-IA

Ce projet a pour objectif de fournir un système de PGI (Plan de Gestion Interne) assisté par Intelligence Artificielle.

## Structure du projet

- `config/` : fichiers de configuration et templates (clés API).
- `docs/` : documentation du projet.
- `src/pgi_ia/` : code source Python du package.
- `tests/` : tests unitaires.
- `data/drop_zone/` : zone de dépôt des fichiers PDF à traiter.

## Mise en route

1. Cloner ce dépôt :
   ```bash
   git clone <URL_DU_REPO>
   cd pgi-ia
   ```
2. Copier `config/agents.example.yaml` en `config/agents.yaml` et renseigner vos clés API.
3. Installer les dépendances (à venir).

## Workflow

1. Déposer un fichier PDF dans `data/drop_zone/`.
2. Exécuter le script de parsing pour extraire les données directives dans un format JSON (à venir).
3. Les données extraites pourront être intégrées dans un tableau HTML ou utilisées dans d'autres étapes du flux.

## Roadmap

- [x] Initialisation et structure du projet.
- [ ] Développement du parser PDF.
- [ ] Intégration dans le hub central.