import json

import paho.mqtt.client as mqtt

from config import MQTT_HOST
from config import MQTT_PORT
from config import MQTT_TOPICS

# from database import Session
from models import SensorReading
from db_worker import enqueue_reading

from state import update


def on_connect(client, userdata, flags, rc, properties=None):

    print("Connected")

    for topic in MQTT_TOPICS:
        client.subscribe(topic)


def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    sensor = payload["sensor"]
    moisture = payload["moisture"]
    temperature = payload["temperature"]
    battery = payload["battery"]

    update(
        sensor,
        moisture,
        temperature,
        battery
    )

    enqueue_reading(payload)


def mqtt_start():

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        MQTT_HOST,
        MQTT_PORT
    )

    client.loop_start()

    return client