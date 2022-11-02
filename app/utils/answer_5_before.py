import mysql.connector
import pandas as pd
from datetime import datetime

connection = mysql.connector.connect(
host = '140.118.157.9',
database = 'foxlink',
user = 'root',
password = 'AqqhQ993VNto',
port='27001',
buffered= True)

cursor = connection.cursor()
mySql_insert_query = f"""SELECT * FROM foxlink.missions m WHERE repair_start_date IS NULL AND is_cancel = 0"""
cursor.execute(mySql_insert_query)
not_assign_mission = cursor.fetchall()

print('\n\n========== NOT ASSIGNED MISSIONS ==========')
print(pd.DataFrame(not_assign_mission).drop(columns=[0,2,3,4,5,6,7,8,10,11]))