from fastapi import FastAPI
import pickle
import numpy as np
import os

# Initialiser l'application FastAPI
app = FastAPI()

# Charger le modèle entraîné
model_path = os.path.join(os.getcwd(), "model", "model.pkl")
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise Exception(f"Le fichier '{model_path}' est introuvable. Vérifiez le chemin et générez le modèle.")

@app.get("/")
def root():
    """
    Endpoint racine.
    """
    return {"message": "Bienvenue dans l'API de prédiction de valeurs immobilières."}

@app.post("/predict/")
def predict(features: dict):
    """
    Endpoint pour effectuer une prédiction.
    :param features: Un dictionnaire contenant les features pour le modèle.
    :return: Une prédiction basée sur les données fournies.
    """
    try:
        # Vérifier que toutes les features requises sont présentes
        required_features = ["longitude", "latitude", "housing_median_age", "total_rooms",
                             "total_bedrooms", "population", "households", "median_income"]
        for feature in required_features:
            if feature not in features:
                return {"error": f"Feature '{feature}' manquante dans les données fournies."}

        # Convertir les features en un tableau NumPy
        X = np.array([list(features.values())])
        # Effectuer la prédiction
        prediction = model.predict(X)[0]
        return {"prediction": prediction}
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}
