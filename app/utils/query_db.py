import mysql.connector

def query_local(query):
    connection = mysql.connector.connect(
    host = '140.118.157.12',
    database = 'foxlink',
    user = 'root',
    password = '123456',
    port='27001',
    buffered= True)

    cursor = connection.cursor()

    cursor.execute(query)
    connection.commit()

    cursor.close()

def query_server(query):
    connection = mysql.connector.connect(
    host = '140.118.157.9',
    database = 'foxlink',
    user = 'root',
    password = 'AqqhQ993VNto',
    port='27001',
    buffered= True)

    cursor = connection.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()

    return data