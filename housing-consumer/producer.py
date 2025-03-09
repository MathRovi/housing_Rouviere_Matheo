from confluent_kafka import Producer
import json
import os

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka-broker:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "housing_topic")

p = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

data = {
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 52,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "median_house_value": 358500,
    "ocean_proximity": "NEAR BAY"
}

p.produce(TOPIC_NAME, key="house", value=json.dumps(data))
p.flush()
print("✅ Message envoyé au topic", TOPIC_NAME)
