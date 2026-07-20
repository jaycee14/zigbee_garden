from queue import Queue

from database import Session
from models import SensorReading
from datetime import datetime, timedelta
from collections import defaultdict

data_queue = Queue()


def enqueue_reading(payload: dict):
    """Called by MQTT thread."""
    data_queue.put(payload)


def db_worker():
    """Runs in a dedicated thread."""

    while True:

        payload = data_queue.get()

        try:
            with Session() as session:
                session.add(
                    SensorReading(
                        sensor=payload["sensor"],
                        moisture=payload["moisture"],
                        temperature=payload["temperature"],
                        battery=payload["battery"],
                    )
                )
                session.commit()

        except Exception as e:
            print("DB write failed:", e)


def get_today():

    midnight = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    try:
        with Session() as session:
            data = Session()\
            .query(SensorReading)\
            .filter(SensorReading.timestamp >= midnight)\
            .order_by(SensorReading.timestamp)\
            .all()

            return format_data(data)

    except Exception as e:
        print("DB read failed:", e)


def format_data(db_ouput):

    output = defaultdict(list)
    for record in db_ouput:
        output[record.sensor].append([record.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),record.moisture])

    return output