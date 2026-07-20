from datetime import datetime, UTC

from sqlalchemy import func

from database import Session
from models import SensorReading


sensor_state = {
    1: {},
    2: {},
    3: {}
}

def update(sensor, moisture, temperature, battery):

    sensor_state[sensor] = {
        "moisture": moisture,
        "temperature": temperature,
        "battery": battery,
        "last_seen": datetime.now(tz=UTC).strftime('%Y-%m-%d %H:%M')
    }

def initialise_sensor_state():

    with Session() as session:

        # Subquery: latest timestamp per sensor
        subq = (
            session.query(
                SensorReading.sensor,
                func.max(SensorReading.timestamp).label("max_ts")
            )
            .group_by(SensorReading.sensor)
            .subquery()
        )

        # Join back to get full rows
        rows = (
            session.query(SensorReading)
            .join(
                subq,
                (SensorReading.sensor == subq.c.sensor) &
                (SensorReading.timestamp == subq.c.max_ts)
            )
            .all()
        )

        for r in rows:

            sensor_state[r.sensor] = {
                "moisture": r.moisture,
                "temperature": r.temperature,
                "battery": r.battery,
                "last_seen": r.timestamp.strftime('%Y-%m-%d %H:%M'),
            }