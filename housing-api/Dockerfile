# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y libpq-dev && apt-get clean

# Copier les fichiers nécessaires dans l'image Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source dans le conteneur
COPY . .

# Lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
