# Utiliser Python 3.11 comme base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du consumer (consumer.py, producer.py, etc.)
COPY . .

# Par défaut, on exécute le consumer
CMD ["python", "consumer.py"]
