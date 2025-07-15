# IA Analyst System

Ce module contient le pipeline d’analyse de données et de génération de vecteurs sémantiques.

## Architecture

- `main.py` : point d’entrée, lit la variable d’environnement `DATA_DIR` et lance le pipeline.
- `pipeline.py` : orchestration des étapes (scan, extraction, embeddings, analyse, stockage).
- `utils.py` : fonctions utilitaires (liste de fichiers, lecture, etc.).

## Utilisation via Docker

1. Placer les données à analyser dans `./data_to_analyze` (lecture seule dans le conteneur).
2. Construire l’image :
   ```bash
   docker compose up --build ia_analyst
   ```
3. Lancer le service :
   ```bash
   docker compose up ia_analyst
   ```

Le répertoire `data_to_analyze` est monté dans `/data` en lecture seule.

## Variables d’environnement

- `OPENAI_API_KEY` : clé API OpenAI pour génération de vecteurs.
- `OLLAMA_ENDPOINT` : URL locale du service Ollama (p.ex. `http://localhost:11434`).
- `OLLAMA_MODEL` : nom du modèle local à utiliser.

## Liste des questions DeepSeek

Avant d’exécuter, créez un fichier `questions.json` à la racine du dossier `ia_analyst` contenant votre jeu de questions :

```json
[
  "Quelle est la politique de sécurité du client ?",
  "Quels sont les processus métiers documentés ?",
  "Quels risques réglementaires sont identifiés ?"
]
```

## Variables d’environnement DeepSeek

- `DEEPSEEK_API_URL` : URL de l’API DeepSeek distante.
- `DEEPSEEK_API_KEY` : Clé API DeepSeek (si nécessaire).
- `DEEPSEEK_LOCAL_URL` : URL du service DeepSeek local (p.ex. `http://localhost:5002`).

L’IA locale appellera d’abord l’API distante, puis le service local pour obtenir les réponses aux questions avant de lancer l’analyse complète.
## Extensions et filtrages

Par défaut, tous les fichiers sont listés. Pour ne traiter que certains types :

```python
# Ex. filtrer seulement .txt et .py
files = list(list_files_recursive(DATA_DIR, extensions=['.txt', '.py']))
```