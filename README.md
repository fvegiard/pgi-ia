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

## Phase 1 – Développement de l'Agent‑Suivi de Directives

1. Préparer un environnement Python :
   ```bash
   cd backend
   python3 -m venv .venv  && source .venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```
2. Copier et compléter la config :
   ```bash
   cp config/agents.example.yaml config/agents.yaml
   # Éditez config/agents.yaml pour y placer vos clés API
   ```
3. Lancer le parser CLI pour extraire les directives :
   ```bash
   scripts/parse_directive.py /chemin/vers/directive.pdf
   ```
   → Génère du JSON avec les champs : id, date_recue, description, prix, po_client, statut
4. Valider la robustesse sur divers formats (CO‑ME, CD, PCE, etc.)

Une fois validé, cochez la case `[ ] Développement du parser PDF.` et intégrez ces sorties dans votre
pipeline de mise à jour du tableau HTML.

## ⚙️ Automatisation GitHub

Pour créer automatiquement le repository GitHub (via un token PAT) et pousser l'initial commit :

```bash
# (Optionnel) Personnalisation :
# export ORG="<organisation_ou_utilisateur>"   # défaut = $(git config user.name)
# export REPO="<nom_du_repo>"                # défaut = pgi-ia
#
export GITHUB_TOKEN=ghp_xxxTON_TOKEN_ICI
bash scripts/create_github_repo.sh
```