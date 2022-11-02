import mysql.connector

connection = mysql.connector.connect(
host = 'localhost',
database = 'foxlink',
user = 'root',
password = '123456',
port='27001')

cursor = connection.cursor()

mySql_insert_query = f"""DELETE FROM foxlink.foxlinkevents"""
cursor.execute(mySql_insert_query)
connection.commit()
mySql_insert_query = f"""DELETE FROM foxlink.testinglogs"""
cursor.execute(mySql_insert_query)
connection.commit()
cursor.close()

connection = mysql.connector.connect(
host = '140.118.157.9',
database = 'foxlink',
user = 'root',
password = 'AqqhQ993VNto',
port='27001')

cursor = connection.cursor()

mySql_insert_query = f"""DELETE FROM foxlink.missions"""
cursor.execute(mySql_insert_query)
connection.commit()

mySql_insert_query = f"""DELETE FROM foxlink.missionevents"""
cursor.execute(mySql_insert_query)
connection.commit()

mySql_insert_query = f"""DELETE FROM foxlink.auditlogheaders"""
cursor.execute(mySql_insert_query)
connection.commit()

cursor.close()