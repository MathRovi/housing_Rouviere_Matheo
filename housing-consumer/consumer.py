from confluent_kafka import Consumer, KafkaError
import requests
import json
import time

# Configuration du consumer Kafka
KAFKA_CONFIG = {
    'bootstrap.servers': 'kafka-broker:9092',
    'group.id': 'housing-consumer-group',
    'auto.offset.reset': 'earliest'
}

TOPIC = 'housing_topic'
API_URL = 'http://api-1:8000/houses'

# URL de MLflow pour les prédictions
MLFLOW_URL = "http://mlflow-model:8001/invocations"

def encode_ocean_proximity(proximity):
    """Convertit la valeur 'ocean_proximity' en variables binaires pour MLflow."""
    categories = ["INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
    return {f"ocean_proximity_{cat}": int(proximity.upper() == cat) for cat in categories}

def consume_messages():
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])

    print("✅ Consumer Kafka démarré...", flush=True)

    try:
        while True:
            msg = consumer.poll(1.0)  # Attendre un message pendant 1 seconde

            if msg is None:
                time.sleep(0.5)  # Éviter de boucler trop vite si aucun message
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"❌ Erreur Kafka: {msg.error()}", flush=True)
                    break

            # Vérifier si le message est vide avant de le traiter
            message_value = msg.value()
            if not message_value:
                print("⚠️ Message vide reçu, ignoré.", flush=True)
                continue

            # Nettoyer les apostrophes parasites
            message_str = message_value.decode('utf-8').strip()
            if message_str.startswith("'") and message_str.endswith("'"):
                message_str = message_str[1:-1]

            # Convertir le message en JSON
            try:
                house = json.loads(message_str)
                print(f"📩 Message reçu : {house}", flush=True)

                # Ajouter les colonnes "ocean_proximity"
                ocean_proximity_encoded = encode_ocean_proximity(house.get("ocean_proximity", ""))

                # ===========================
                # 1) APPEL À MLflow POUR LA PRÉDICTION
                # ===========================
                payload = {
                    "dataframe_split": {
                        "columns": [
                            "longitude",
                            "latitude",
                            "housing_median_age",
                            "total_rooms",
                            "total_bedrooms",
                            "population",
                            "households",
                            "median_income",
                            "ocean_proximity_INLAND",
                            "ocean_proximity_ISLAND",
                            "ocean_proximity_NEAR BAY",
                            "ocean_proximity_NEAR OCEAN"
                        ],
                        "data": [[
                            house.get("longitude", 0),
                            house.get("latitude", 0),
                            house.get("housing_median_age", 0),
                            house.get("total_rooms", 0),
                            house.get("total_bedrooms", 0),
                            house.get("population", 0),
                            house.get("households", 0),
                            house.get("median_income", 0),
                            ocean_proximity_encoded["ocean_proximity_INLAND"],
                            ocean_proximity_encoded["ocean_proximity_ISLAND"],
                            ocean_proximity_encoded["ocean_proximity_NEAR BAY"],
                            ocean_proximity_encoded["ocean_proximity_NEAR OCEAN"]
                        ]]
                    }
                }

                print(f"🔍 Payload envoyé à MLflow: {json.dumps(payload, indent=2)}", flush=True)

                try:
                    resp = requests.post(MLFLOW_URL, json=payload)
                    resp.raise_for_status()
                    prediction = resp.json()["predictions"][0]
                    print(f"🔮 Predicted house value: {prediction}", flush=True)
                    house["estimated_median_house_value"] = prediction
                except requests.exceptions.RequestException as e:
                    print(f"❌ Erreur MLflow: {e}", flush=True)
                    house["estimated_median_house_value"] = 0.0

                # ===========================
                # 2) ENVOYER LA MAISON + PRED À L'API
                # ===========================
                print(f"📤 Envoi à l'API : {json.dumps(house, indent=2)}", flush=True)
                response = requests.post(API_URL, json=house)
                response.raise_for_status()
                print(f"✅ Données envoyées à l'API: {response.json()}", flush=True)

            except json.JSONDecodeError:
                print(f"❌ Erreur: Impossible de décoder le message JSON, message corrompu: {message_str}", flush=True)
                continue

    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du consumer Kafka...", flush=True)
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
