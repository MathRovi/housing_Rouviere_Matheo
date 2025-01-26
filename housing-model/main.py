from fastapi import FastAPI
import pickle
import numpy as np

# Initialiser l'application FastAPI
app = FastAPI()

# Charger le modèle entraîné
try:
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise Exception("Le fichier 'model/model.pkl' est introuvable. Assurez-vous de l'avoir généré avec train_model.py.")

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
        # Convertir les features en un tableau NumPy
        X = np.array([list(features.values())])
        # Effectuer la prédiction
        prediction = model.predict(X)[0]
        return {"prediction": prediction}
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}
