import mysql.connector
import pandas as pd
from datetime import datetime

ip = '127.0.0.1'

connection = mysql.connector.connect(
host = ip,
database = 'testing_api',
user = 'root',
password = 'AqqhQ993VNto',
port='27001',
buffered= True)

cursor = connection.cursor()

mySql_insert_query = f"""SELECT * FROM testing_api.audit_log_headers"""
cursor.execute(mySql_insert_query)
data = cursor.fetchall()
cursor.close()

table = pd.DataFrame(data)
table.rename(columns={0:'id', 1:'action', 2:'table_name', 3:'record_pk', 4:'user', 5:'created_date', 6:'description'}, inplace=True)
result = {}

for i in range(1, 201):
    name = 'C0{}'.format(str(i).zfill(3))
    result[name] = {
        'login': 0,
        'logout': 0,
        'last_loging': None,
        'period': [],
        'avg': 0,
        'is_correct': False
    }
    
result['admin'] = {
        'login': 0,
        'logout': 0,
        'last_loging': None,
        'period': [],
        'avg': 0,
        'is_correct': False
    }

for index, row in table.iterrows():
    start, end = None, None
    if row['action'] == 'USER_LOGIN':
        result[row['user']]['last_loging'] = row['created_date']
        result[row['user']]['login'] += 1
    elif row['action'] == 'USER_LOGOUT':
        start = result[row['user']]['last_loging']
        end = row['created_date']
        
        result[row['user']]['logout'] += 1
        result[row['user']]['period'].append((end - start) / pd.Timedelta(seconds=1))
        
total_avg = 0

for i in range(1, 201):
    name = 'C0{}'.format(str(i).zfill(3))
    if len(result[name]['period']) != 0:
        result[name]['avg'] = sum(result[name]['period']) / len(result[name]['period'])
    total_avg += result[name]['avg']
    if result[name]['login'] == result[name]['logout'] and result[name]['login'] == 100:
        result[name]['is_correct'] = True
    
total_avg /= 200

answer = pd.DataFrame.from_dict(result, orient='index').drop(['last_loging', 'period'], axis=1)

print(answer.to_string())
print("avg: ", total_avg)