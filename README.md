# Housing Prediction API - Projet de Matheo Rouvière

## Description
Ce projet implémente une API permettant de prédire la valeur médiane des maisons en fonction de diverses caractéristiques comme la localisation géographique, l'âge des maisons, le nombre de chambres, le revenu médian, etc. Le modèle utilisé pour faire ces prédictions est un modèle de régression linéaire, entraîné sur un jeu de données de logements. L'API est développée avec **FastAPI** et le modèle est créé avec **scikit-learn**.

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés :

- **Python 3.11.9**
- **Docker** 
- **Git**

## Installation

1. Cloner le projet

Clonez le projet depuis GitHub :
git clone https://github.com/MathRovi/housing_Rouviere_Matheo.git
cd housing_Rouviere_Matheo

## Dans le dossier housing-model, créez un environnement virtuel pour installer les dépendances

cd housing-model
python -m venv venv

## Ensuite, activez l'environnement virtuel:
venv\scripts\activate (pour windows)
source venv/bin/activate (pour linux, macOS)

## 3. Installer les dépendances
Installez les dépendances nécessaires avec la commande suivante :
pip install -r requirements.txt

