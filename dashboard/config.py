MQTT_HOST = "localhost"
MQTT_PORT = 1883

MQTT_TOPICS = [
    "garden/sensor1",
    "garden/sensor2",
    "garden/sensor3",
]

DATABASE_URL = "sqlite:///sensors.db"

OFFLINE_TIMEOUT = 600       # seconds