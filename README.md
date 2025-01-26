# Housing Prediction API - Projet de Matheo Rouvière

# Description
Ce projet implémente une API permettant de prédire la valeur médiane des maisons en fonction de diverses caractéristiques comme la localisation géographique, l'âge des maisons, le nombre de chambres, le revenu médian, etc. Le modèle utilisé pour faire ces prédictions est un modèle de régression linéaire, entraîné sur un jeu de données de logements. L'API est développée avec **FastAPI** et le modèle est créé avec **scikit-learn**.

# Prérequis

## Avant de commencer, assurez-vous d'avoir les outils suivants installés :

- **Python 3.11.9**
- **Docker** 
- **Git**

# Installation

# 1. Cloner le projet

## Clonez le projet depuis GitHub :

git clone https://github.com/MathRovi/housing_Rouviere_Matheo.git

cd housing_Rouviere_Matheo

# Dans le dossier housing-model, créez un environnement virtuel pour installer les dépendances

cd housing-model

python -m venv venv

# 2. Ensuite, activez l'environnement virtuel:

venv\scripts\activate (pour windows)

source venv/bin/activate (pour linux, macOS)

# 3. Installer les dépendances
## Installez les dépendances nécessaires avec la commande suivante :

pip install -r requirements.txt

# 4. Entraîner le modèle
## Dans le dossier housing-model, exécutez le script Python pour entraîner le modèle de régression linéaire :

python train_model.py

## Cela génère le modèle et le sauvegarde dans le fichier model/model.pkl.

# Démarrer le projet
# 1. Démarrer l'API avec FastAPI
## Allez dans le dossier housing-api et démarrez le serveur FastAPI avec la commande suivante :

cd housing-api

uvicorn main:app --reload

## Cela démarre le serveur API à l'adresse http://localhost:8000.

# 2. Démarrer le projet avec Docker

## Si vous souhaitez exécuter le projet avec Docker, vous pouvez utiliser docker-compose.

## Construire les images Docker :

docker-compose build

# Démarrer les containers :

docker-compose up

## Les services seront en cours d'exécution dans les containers Docker. L'API sera accessible via http://localhost:8000.

# Utilisation de l'API
## L'API expose un endpoint pour prédire la valeur médiane des maisons en fonction de plusieurs paramètres.

POST /predict/ : Prédire la valeur médiane des maisons en fonction des paramètres fournis.

## Exemple de données sous le format JSON à envoyer :

{
  "longitude": -122.23,
  "latitude": 37.88,
  "housing_median_age": 41.0,
  "total_rooms": 880,
  "total_bedrooms": 129,
  "population": 322,
  "households": 126,
  "median_income": 8.3252,
  "ocean_proximity_INLAND": 0,
  "ocean_proximity_NEAR BAY": 1,
  "ocean_proximity_NEAR OCEAN": 0,
  "ocean_proximity_ISLAND": 0
}

## Réponse attendue :

{
  "prediction": 628725.5062235147
}
Tests
Des tests unitaires sont intégrés dans le projet pour tester l'API. Vous pouvez utiliser des outils comme Postman ou Swagger UI pour tester les points de terminaison. Swagger UI est accessible à l'adresse http://localhost:8000/docs.
