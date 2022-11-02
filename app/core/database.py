from asyncio import events
from pydantic import Json
from sqlalchemy import MetaData, create_engine
import datetime
import databases
import ormar
from app.env import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_NAME
)

DATABASE_URI = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

database = databases.Database(DATABASE_URI)
metadata = MetaData()

class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

class FoxlinkEvent(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    category: int = ormar.Integer(nullable=True)
    message: str = ormar.String(max_length=100, nullable=True)
    project: str = ormar.String(max_length=100, nullable=True)
    line: str = ormar.String(max_length=100, nullable=True)
    device_name: str = ormar.String(max_length=100, nullable=True)
    start_time: datetime = ormar.DateTime(nullable=True)
    end_time: datetime = ormar.DateTime(nullable=True)
    start_file_name: str = ormar.String(max_length=10, nullable=True)
    end_file_name: str = ormar.String(max_length=10, nullable=True)
    event_id: int = ormar.Integer()

class TestingLog(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    mission_id: int = ormar.Integer(nullable=True)
    mqtt: str = ormar.String(max_length=100, nullable=True)
    username: str = ormar.String(max_length=100, nullable=True)
    action: str = ormar.String(max_length=100, nullable=True)
    description: str = ormar.String(max_length=200, nullable=True)
    mqtt_detail = ormar.Text(nullable=True)
    time: datetime = ormar.DateTime(nullable=True)


engine = create_engine(DATABASE_URI)

metadata.create_all(engine)