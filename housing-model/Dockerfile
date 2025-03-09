# Dockerfile pour housing-model

FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Installer MLflow avec les versions exactes pour éviter les conflits
RUN pip install --no-cache-dir mlflow==2.20.0 numpy==2.2.2 scipy==1.15.1 gunicorn

# Copier le répertoire des artefacts
COPY ./mlruns /app/mlruns

# Exposer le port du modèle
EXPOSE 8001

# Commande pour lancer le modèle MLflow
CMD ["mlflow", "models", "serve", "-m", "file:///app/mlruns/817329415073338012/ef505ee1b5714854a79b4e489b4ad11d/artifacts/model", "--no-conda", "-h", "0.0.0.0", "-p", "8001"]
