# Housing Prediction API - Projet de Matheo Rouvière

## Description
Ce projet implémente une API permettant de prédire la valeur médiane des maisons en fonction de diverses caractéristiques comme la localisation géographique, l'âge des maisons, le nombre de chambres, le revenu médian, etc. Le modèle utilisé pour faire ces prédictions est un modèle de régression linéaire, entraîné sur un jeu de données de logements. L'API est développée avec FastAPI et le modèle est géré avec MLflow pour le suivi des expérimentations et le déploiement.

---

## Prérequis
Avant de commencer, assurez-vous d'avoir les outils suivants installés :
- **Python 3.11.9**
- **Docker**
- **Git**

---

## Installation

### 1. Cloner le projet
Clonez le projet depuis GitHub :
```bash
git clone https://github.com/MathRovi/housing_Rouviere_Matheo.git
cd housing_Rouviere_Matheo
```

### 2. Installer les dépendances

#### a. Créer un environnement virtuel (optionnel mais recommandé)
Dans le dossier `housing-model`, créez un environnement virtuel :
```bash
cd housing-model
python -m venv venv
```

#### b. Activer l'environnement virtuel
- Pour **Windows** :
  ```bash
  venv\scripts\activate
  ```
- Pour **Linux/MacOS** :
  ```bash
  source venv/bin/activate
  ```

#### c. Installer les dépendances Python
Installez les dépendances nécessaires avec la commande suivante :
```bash
pip install -r requirements.txt
```

### 3. Entraîner le modèle
Dans le dossier `housing-model`, exécutez le script Python pour entraîner le modèle de régression linéaire :
```bash
python train_model.py
```
Cela génère le modèle et le sauvegarde dans le fichier `model/model.pkl`.

---

## Étape 4 : Utilisation de MLflow pour le suivi des expérimentations et la gestion des modèles

### Suivi des expérimentations
1. **Installation de MLflow** :
   Si ce n'est pas déjà fait, installez MLflow dans votre environnement avec la commande suivante :
   ```bash
   pip install mlflow
   ```

2. **Démarrer l'interface MLflow** :
   Dans le dossier `housing-model`, démarrez le serveur MLflow :
   ```bash
   mlflow ui
   ```
   Cela ouvre une interface web accessible à l'adresse `http://localhost:5000`.

3. **Enregistrer les expérimentations** :
   Pendant l'entraînement du modèle, les paramètres, métriques et artefacts sont automatiquement enregistrés dans MLflow grâce aux fonctions :
   - `log_params` pour les hyperparamètres
   - `log_metrics` pour les résultats d'évaluation
   - `log_model` pour sauvegarder le modèle entraîné.

4. **Ajouter le modèle au registre de modèles** :
   Une fois un modèle satisfaisant obtenu, vous pouvez l'ajouter au registre de modèles via l'interface MLflow ou via le script `promote_model.py`.

---

## Étape 5 : Déploiement avec MLflow Model Server

### Création et déploiement
1. **Créer une image Docker pour le modèle** :
   Utilisez MLflow pour construire une image Docker pour le modèle. Dans le dossier `housing-model`, exécutez :
   ```bash
   mlflow models build-docker -m ./mlruns/817329415073338012/ef505ee1b5714854a79b4e489b4ad11d/artifacts/model -n housing-model
   ```
   Cette commande crée une image Docker contenant une API REST pour le modèle.

2. **Configurer `docker-compose`** :
   La configuration de `docker-compose.yaml` a été mise à jour pour inclure le modèle MLflow en tant que service (`model-1`).

3. **Démarrer les services Docker** :
   - Construire les images Docker :
     ```bash
     docker-compose build
     ```
   - Démarrer les containers :
     ```bash
     docker-compose up
     ```
   L'API FastAPI est accessible sur `http://localhost:8000` et le modèle MLflow est disponible sur `http://localhost:8001`.

---

## Etape 6 : 
### Topic Kafka
docker exec -it kafka-broker /usr/bin/kafka-topics --bootstrap-server kafka-broker:9092 --list

### Logs du consumer:
docker logs housing-consumer --follow

## Etape 7 : Envoi de messages (Producer)
### Option A : via docker-compose run housing-producer

docker-compose run housing-producer

Cela envoie un fichier Json a housing_topic

### Le consumer lira ce message et appellera POST /houses. Vérifie via :
curl -X GET http://127.0.0.1:8000/houses

## Utilisation de l'API

### Endpoints principaux
- **`POST /predict/`** : Prédire la valeur médiane des maisons.

### Exemple de requête Curl pour recevoir une reponse valide de la part d'MLflow dans le cmd windows
#### Requête
curl -X POST http://127.0.0.1:8001/invocations -H "Content-Type: application/json" -d "{\"dataframe_records\": [{\"longitude\": -122.23, \"latitude\": 37.88, \"housing_median_age\": 41, \"total_rooms\": 880, \"total_bedrooms\": 129, \"population\": 322, \"households\": 126, \"median_income\": 8.3252, \"ocean_proximity_INLAND\": false, \"ocean_proximity_ISLAND\": false, \"ocean_proximity_NEAR BAY\": false, \"ocean_proximity_NEAR OCEAN\": false}]}"

#### Réponse attendue
{"predictions": [415072.13176069316]}

### Commande pour tester FastApi dans le cmd Windows:
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\"inputs\": [[-122.23, 37.88, 41, 880, 129, 322, 126, 8.3252, 0, 0, 0, 0]]}"

## Utilisez les fonctionnalités intégrées de FastAPI pour documenter l'API avec Swagger (accessible à http://127.0.0.1:8000/docs).
### A insérer dans /predict

{
  "inputs": [[-122.23, 37.88, 41, 880, 129, 322, 126, 8.3252, 0, 0, 0, 0]]
} 

## Documentation supplémentaire
- **MLflow** :
  - [Getting Started](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html)
  - [Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- **Docker** :
  - [Docker Compose](https://docs.docker.com/compose/)
```

