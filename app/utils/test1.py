import mysql.connector
import pandas as pd
from datetime import datetime

ip = '127.0.0.1'

connection = mysql.connector.connect(
host = ip,
database = 'testing_foxlink',
user = 'root',
password = 'AqqhQ993VNto',
port='27001',
buffered= True)

cursor = connection.cursor()

mySql_insert_query = f"""SELECT * FROM testing_foxlink.testinglogs"""
cursor.execute(mySql_insert_query)
data_log = cursor.fetchall()

cursor.close()

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
data_audit = cursor.fetchall()

mySql_insert_query = f"""SELECT m.device, m.worker, m.is_done , m.accept_recv_date ,m.repair_beg_date ,m.repair_end_date ,m.created_date, m.notify_send_date, m.id  FROM testing_api.missions m """
cursor.execute(mySql_insert_query)
data_mission = cursor.fetchall()

cursor.close()

table_audit = pd.DataFrame(data_audit)
table_audit.rename(columns={0:'id', 1:'action', 2:'table_name', 3:'record_pk', 4:'user', 5:'created_date', 6:'description'}, inplace=True)

table_mission = pd.DataFrame(data_mission)
table_mission.rename(columns={0:'device', 1:'worker', 2:'is_done', 3:'accept_recv_date', 4:'repair_beg_date', 5:'repair_end_date', 6:'created_date', 7:'notify_send_date', 8:'id'}, inplace=True)
table_mission

table_log = pd.DataFrame(data_log)
table_log.rename(columns={0:'id', 1:'mission_id', 2:'mqtt', 3:'username', 4:'action', 5:'description', 6:'mqtt_detail', 7:'time'}, inplace=True)

result_user = {}
USER_NUMBER = 91

for i in range(1, USER_NUMBER + 1):
    name = 'C0{}'.format(str(i).zfill(3))
    result_user[name] = {
        'login': None,
        'logout': None,
        'assign': [],
        'accept': [],
        'reject': [],
        'start': [],
        'repair_start_date': [],
        'repair_end_date': [],
        'mission_id': [],
        'is_correct': False
    }

for index, row in table_log.iterrows():
    if row['action'] == 'login':
        result_user[row['username']]['login'] = row['time']
    elif row['action'] == 'logout':
        result_user[row['username']]['logout'] = row['time']
    elif row['action'] == 'accept' and row['description'] == 'API_200':
        result_user[row['username']]['accept'].append(row['time'])
    elif row['action'] == 'start' and row['description'] == 'API_200':
        result_user[row['username']]['is_correct'] = True
        result_user[row['username']]['start'].append(row['time'])
    elif row['action'] == 'reject' and row['description'] == 'API_200':
        result_user[row['username']]['reject'].append(row['time'])
        
for index, row in table_audit.iterrows():
    if row['action'] == 'MISSION_ASSIGNED':
        result_user[row['user']]['assign'].append(row['created_date'])
        result_user[row['user']]['mission_id'].append(row['record_pk'])
        
for index, row in table_mission.iterrows():
    result_user[row['worker']]['repair_start_date'] = row['repair_beg_date']
    result_user[row['worker']]['repair_end_date'] = row['repair_end_date']

answer_user = pd.DataFrame.from_dict(result_user, orient='index')
print('\n\n========== USER BASE ==========\n\n')
print(answer_user.to_string())

result_mission = {}
mission_id = table_mission['id'].unique()
mission = {}
period = []

for m in mission_id:
    cursor = connection.cursor()

    mySql_insert_query = f"""SELECT created_date from testing_api.audit_log_headers a WHERE a.record_pk = '{m}' and a.`action` = 'MISSION_ASSIGNED'"""
    cursor.execute(mySql_insert_query)
    assign_date = cursor.fetchone()
    if assign_date:
        assign_date = pd.DataFrame(assign_date)[0][0]
    
    mySql_insert_query = f"""SELECT created_date from testing_api.audit_log_headers a WHERE a.record_pk = '{m}' and a.`action` = 'MISSION_ACCEPTED'"""
    cursor.execute(mySql_insert_query)
    accept_date = cursor.fetchone()
    if accept_date:
        accept_date = pd.DataFrame(accept_date)[0][0]
        period.append((accept_date - assign_date) / pd.Timedelta(seconds=1))

    cursor.close()
    
    mission[m] = {
        'assign_date': assign_date,
        'acept_date': accept_date,
        'is_accept': True if accept_date else False
    }

for index, row in table_mission.iterrows():
    result_mission[row['id']] = {
        'mission_id': row['id'],
        'device': row['device'],
        'mission_created_date': row['created_date'],
        'assign': mission[row['id']]['assign_date'],
        'assignee': row['worker'],
        'is_accept': mission[row['id']]['is_accept'],
        'is_correcct': True if mission[row['id']]['is_accept'] else False
    }

answer_mission = pd.DataFrame.from_dict(result_mission, orient='index')
print('\n\n========== MISSION BASE ==========\n\n')
print(answer_mission.to_string())

print('\n\n========== MISSION ASSIGN -> ACCEPTED AVG ==========')
print(sum(period) / len(period))

cursor = connection.cursor()
mySql_insert_query = f"""SELECT * FROM testing_api.missions m WHERE repair_beg_date IS NULL AND is_done = 0"""
cursor.execute(mySql_insert_query)
not_assign_mission = cursor.fetchall()

print('\n\n========== NOT ASSIGNED MISSIONS ==========')
print(pd.DataFrame(not_assign_mission))