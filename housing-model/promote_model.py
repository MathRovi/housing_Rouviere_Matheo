from mlflow.tracking import MlflowClient

# Créer un client MLflow
client = MlflowClient()

# Informations sur le modèle et la version
model_name = "Housing-Model-Matheo.R"  # Remplacez par le nom de votre modèle enregistré
model_version = 1  # La version du modèle que vous voulez promouvoir
alias_name = "production"  # Nom de l'alias (vous pouvez le personnaliser)

# Ajouter ou mettre à jour un alias pour la version du modèle
client.set_registered_model_alias(
    name=model_name,
    alias=alias_name,
    version=model_version,
)

print(f"Le modèle '{model_name}' version {model_version} a été associé à l'alias '{alias_name}'.")
