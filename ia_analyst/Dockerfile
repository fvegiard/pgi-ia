FROM python:3.12-slim

# Installer les dépendances système pour compilation si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l’analyse
COPY . /app

# Dossier des données monté en lecture seule
ENV DATA_DIR=/data

# Lancement du pipeline d’analyse
CMD ["python", "main.py"]