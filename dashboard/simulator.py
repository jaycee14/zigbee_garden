import json
import random
import time

import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883)

state = {
    1: {"moisture": 72, "temperature": 21.4, "battery": 96},
    2: {"moisture": 61, "temperature": 22.1, "battery": 91},
    3: {"moisture": 84, "temperature": 20.7, "battery": 98},
}

while True:

    for sensor, values in state.items():

        values["moisture"] += random.randint(-2, 2)
        values["temperature"] += random.uniform(-0.2, 0.2)
        values["battery"] -= random.uniform(0.0005, 0.002)

        values["moisture"] = max(0, min(100, values["moisture"]))
        values["battery"] = max(0, values["battery"])

        payload = {
            "sensor": sensor,
            "moisture": round(values["moisture"], 1),
            "temperature": round(values["temperature"], 1),
            "battery": round(values["battery"], 1),
        }

        client.publish(
            f"garden/sensor{sensor}",
            json.dumps(payload),
        )

    time.sleep(10)