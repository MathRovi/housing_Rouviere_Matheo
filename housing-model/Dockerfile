# Utilise une image légère de Python
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt requirements.txt

# Installe les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie tous les fichiers de l'application dans le conteneur
COPY . .

# Expose le port utilisé par l'API
EXPOSE 8001

# Commande pour démarrer le service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
