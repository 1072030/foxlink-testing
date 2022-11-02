import asyncio, json
from datetime import datetime
import logging
from app.core.database import TestingLog, database
import mysql.connector
from app.env import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USER, DATABASE_NAME


async def log(param, sem):
    async with sem:
        await TestingLog.objects.create(
            mission_id = param['mission_id'],
            mqtt = param['mqtt'],
            username = param['username'],
            action = param['action'],
            description =param['description'],
            mqtt_detail = param['mqtt_detail'],
            time = param['time'],
        )

def create_log(param):
    try:
        CONNECTION = mysql.connector.connect(
        host = DATABASE_HOST,
        database = DATABASE_NAME,
        user = DATABASE_USER,
        password = DATABASE_PASSWORD)
        
        cursor = CONNECTION.cursor()

        mySql_insert_query = "INSERT INTO testinglogs (mission_id, mqtt, username, action, description, mqtt_detail, time) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}');".format(
            param['mission_id'], param['mqtt'], param['username'], param['action'], param['description'], param['mqtt_detail'].replace("'", "\\\'"), param['time'].strftime('%Y-%m-%d  %H:%M:%S')
        )
        cursor.execute(mySql_insert_query)
        CONNECTION.commit()
        cursor.close()
    except:
        logging.warning(mySql_insert_query)
        logging.warning(f"{param['username']} can't create log")
    

async def database_connect():
    await database.connect()

def connect_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database_connect())