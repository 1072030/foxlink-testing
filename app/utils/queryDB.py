import mysql.connector
from app.env import (
        FOXLINK_DATABASE_HOST,
        FOXLINK_DATABASE_PORT,
        FOXLINK_DATABASE_USER,
        FOXLINK_DATABASE_PASSWORD,
        FOXLINK_DATABASE_NAME,
    )

def query_testing(query):
    connection = mysql.connector.connect(
    host = FOXLINK_DATABASE_HOST,
    database = FOXLINK_DATABASE_NAME,
    user = FOXLINK_DATABASE_USER,
    password = FOXLINK_DATABASE_PASSWORD,
    port=FOXLINK_DATABASE_PORT,
    buffered= True)

    cursor = connection.cursor()

    cursor.execute(query)
    connection.commit()

    cursor.close()

def query_server(query):
    connection = mysql.connector.connect(
        host = FOXLINK_DATABASE_HOST,
        database = "foxlink",
        user = FOXLINK_DATABASE_USER,
        password = FOXLINK_DATABASE_PASSWORD,
        port=FOXLINK_DATABASE_PORT,
    buffered= True)

    cursor = connection.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()

    return data