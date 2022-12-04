import asyncio, json
from datetime import datetime, timedelta
import logging
from app.services.database import TestingLog, database
import mysql.connector
from app.env import FOXLINK_DATABASE_HOST, FOXLINK_DATABASE_PASSWORD, FOXLINK_DATABASE_USER, FOXLINK_DATABASE_NAME, TESTING_LOG


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
    if TESTING_LOG:
        try:
            CONNECTION = mysql.connector.connect(
                host = FOXLINK_DATABASE_HOST,
                database = FOXLINK_DATABASE_NAME,
                port = 27001,
                user = FOXLINK_DATABASE_USER,
                password = FOXLINK_DATABASE_PASSWORD
            )
            
            cursor = CONNECTION.cursor()

            mySql_insert_query = "INSERT INTO testinglogs (mission_id, mqtt, username, action, description, mqtt_detail, time) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}');".format(
                param['mission_id'], param['mqtt'], param['username'], param['action'], param['description'], param['mqtt_detail'].replace("'", "\\\'"), param['time'].strftime('%Y-%m-%d  %H:%M:%S')
            )
            cursor.execute(mySql_insert_query)
            CONNECTION.commit()
            cursor.close()
        except Exception as e:
            logging.warning(e)
    
def kill_process():
    connection = mysql.connector.connect(
    host = '140.118.157.9',
    database = 'foxlink',
    user = 'root',
    password = 'AqqhQ993VNto',
    port='27001')

    cursor = connection.cursor()

    mySql_insert_query = """SELECT ID FROM information_schema.processlist WHERE (COMMAND = "Query" or COMMAND = 'Sleep') and Time > 30"""
    cursor.execute(mySql_insert_query)
    id = cursor.fetchall()

    for i in id:
        mySql_insert_query = f"KILL {i[0]}"
        cursor.execute(mySql_insert_query)
        cursor.fetchall()
        
    cursor.close()

async def database_connect():
    await database.connect()

def connect_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database_connect())