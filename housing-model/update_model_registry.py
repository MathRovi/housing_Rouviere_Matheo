import mlflow
from mlflow.tracking import MlflowClient

# Nom du modèle dans le Model Registry
model_name = "Housing-Model-Matheo.R"

# Description et tags à ajouter
model_description = "Modèle amélioré de prédiction des prix des maisons, basé sur des données prétraitées et optimisées."
model_tags = {
    "Version": "1.0",
    "Auteur": "Matheo Rouviere",
    "Type": "Regression linéaire",
    "Dataset": "California Housing Dataset",
    "RMSE": "2190144091.692922",
    "R2": "0.72"
}

# Initialiser le client MLflow
client = MlflowClient()

# Mettre à jour la description
client.update_registered_model(
    name=model_name,
    description=model_description
)

# Ajouter les tags au modèle
for key, value in model_tags.items():
    client.set_registered_model_tag(name=model_name, key=key, value=value)

print(f"Description et tags ajoutés au modèle {model_name}.")
