import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import os

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
print(f"Mean Squared Error: {mse}")

# Sauvegarder le modèle entraîné dans un fichier
os.makedirs("model", exist_ok=True)
model_path = "model/model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print(f"Modèle sauvegardé dans '{model_path}'")
