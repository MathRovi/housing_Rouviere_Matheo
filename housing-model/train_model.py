import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os
import pickle  # Ajout de l'importation du module pickle

# Démarrer un run MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

mlflow.set_experiment("Improved Housing Price PredictionV2")

with mlflow.start_run():
    # Charger le fichier CSV
    data_path = "housing.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Le fichier {data_path} est introuvable.")

    data = pd.read_csv(data_path)

    # Préparer les données en supprimant les lignes avec des valeurs manquantes
    data = data.dropna()

    # Séparer les variables explicatives (X) et la variable cible (y)
    X = data.drop("median_house_value", axis=1)
    y = data["median_house_value"]

    # Convertir la colonne catégorielle "ocean_proximity" en variables numériques (one-hot encoding)
    X = pd.get_dummies(X, columns=["ocean_proximity"], drop_first=True)

    # Diviser les données en ensemble d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner un modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Évaluer le modèle avec l'erreur quadratique moyenne
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = model.score(X_test, y_test)

    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")

    # Loguer les hyperparamètres, métriques et le modèle
    mlflow.log_params({
        "test_size": 0.2,
        "random_state": 42,
        "model_type": "LinearRegression"
    })

    mlflow.log_metrics({
        "mse": mse,
        "r2": r2
    })

    # Inférer la signature du modèle
    signature = infer_signature(X_train, model.predict(X_train))
    input_example = X_train.head(1)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="mlflow_model",
        signature=signature,
        input_example=input_example
    )

    # Sauvegarder localement le modèle
    os.makedirs("model", exist_ok=True)
    model_path = "model/improved_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)  # Utilisation correcte de pickle
    print(f"Improved model saved to '{model_path}'")
