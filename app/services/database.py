from pydantic import Json
from sqlalchemy import MetaData, create_engine
from datetime import timedelta, datetime
from typing import Optional, List, ForwardRef
from enum import Enum
from ormar import property_field, pre_update
from sqlalchemy import MetaData, create_engine
from sqlalchemy.sql import func
import databases
import ormar
import sqlalchemy
import uuid
import asyncio
from app.env import (
    FOXLINK_DATABASE_HOST,
    FOXLINK_DATABASE_PORT,
    FOXLINK_DATABASE_USER,
    FOXLINK_DATABASE_PASSWORD,
    FOXLINK_DATABASE_NAME,
)

DATABASE_URI = f"mysql://{FOXLINK_DATABASE_USER}:{FOXLINK_DATABASE_PASSWORD}@{FOXLINK_DATABASE_HOST}:{FOXLINK_DATABASE_PORT}/{FOXLINK_DATABASE_NAME}"

database = databases.Database(DATABASE_URI, max_size=10)

metadata = MetaData()

MissionRef = ForwardRef("Mission")

AuditLogHeaderRef = ForwardRef("AuditLogHeader")


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class FoxlinkEvent(ormar.Model):
    class Meta(MainMeta):
        tablename="foxlink_event_new"

    id: int = ormar.Integer(primary_key=True)
    line: str = ormar.String(max_length=100, nullable=True)
    device_name: str = ormar.String(max_length=100, nullable=True)
    category: int = ormar.Integer(nullable=True)
    start_time: datetime = ormar.DateTime(nullable=True)
    end_time: datetime = ormar.DateTime(nullable=True)
    message: str = ormar.String(max_length=100, nullable=True)
    start_file_name: str = ormar.String(max_length=10, nullable=True)
    end_file_name: str = ormar.String(max_length=10, nullable=True)
    project: str = ormar.String(max_length=100, nullable=True)
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
