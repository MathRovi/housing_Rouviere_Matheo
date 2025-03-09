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

            # 🔥 CORRECTION : Nettoyer les apostrophes parasites 🔥
            message_str = message_value.decode('utf-8').strip()
            if message_str.startswith("'") and message_str.endswith("'"):
                message_str = message_str[1:-1]

            # Convertir le message en JSON
            try:
                message_data = json.loads(message_str)
                print(f"📩 Message reçu : {message_data}", flush=True)

                # Envoyer les données à `housing-api`
                response = requests.post(API_URL, json=message_data)
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
