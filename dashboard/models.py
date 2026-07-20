from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SensorReading(Base):

    __tablename__ = "soil_sensor_readings"

    id = Column(Integer, primary_key=True)
    sensor = Column(Integer)
    moisture = Column(Float)
    temperature = Column(Float)
    battery = Column(Float)
    timestamp = Column(DateTime, default=datetime.now(tz=UTC))