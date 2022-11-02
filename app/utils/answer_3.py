import mysql.connector
import pandas as pd
from datetime import datetime

connection = mysql.connector.connect(
host = 'localhost',
database = 'foxlink',
user = 'root',
password = '123456',
port='27001',
buffered= True)

cursor = connection.cursor()

mySql_insert_query = f"""SELECT * FROM foxlink.testinglogs"""
cursor.execute(mySql_insert_query)
data_log = cursor.fetchall()

cursor.close()

connection = mysql.connector.connect(
host = '140.118.157.9',
database = 'foxlink',
user = 'root',
password = 'AqqhQ993VNto',
port='27001',
buffered= True)

cursor = connection.cursor()

mySql_insert_query = f"""SELECT * FROM foxlink.auditlogheaders"""
cursor.execute(mySql_insert_query)
data_audit = cursor.fetchall()

mySql_insert_query = f"""SELECT e.mission, event_id, device, user, repair_start_date, repair_end_date, created_date, event_start_date, event_end_date  from foxlink.missionevents e
inner join foxlink.missions m on m.id = e.mission
inner join foxlink.missions_users mu on m.id = mu.mission 
order by mission"""
cursor.execute(mySql_insert_query)
data_mission = cursor.fetchall()

cursor.close()

table_audit = pd.DataFrame(data_audit)
table_audit.rename(columns={0:'id', 1:'action', 2:'table_name', 3:'record_pk', 4:'user', 5:'created_date', 6:'description'}, inplace=True)

table_mission = pd.DataFrame(data_mission)
table_mission.rename(columns={0:'mission', 1:'event_id', 2:'device', 3:'user', 4:'repair_start_date', 5:'repair_end_date', 6:'created_date', 7:'event_start_date', 8:'event_end_date', 9:'created_date', 10:'updated_date', 11:'is_autocanceled'}, inplace=True)

table_log = pd.DataFrame(data_log)
table_log.rename(columns={0:'id', 1:'mission_id', 2:'mqtt', 3:'username', 4:'action', 5:'description', 6:'mqtt_detail', 7:'time'}, inplace=True)

result_user = {}
USER_NUMBER = 91
period = []

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
        'is_correct': False,
        'rescue': False
    }

for index, row in table_log.iterrows():
    if row['action'] == 'login':
        result_user[row['username']]['login'] = row['time']
    elif row['action'] == 'logout':
        result_user[row['username']]['logout'] = row['time']
    elif row['action'] == 'accept' and row['description'] == 'API_200':
        result_user[row['username']]['accept'].append(row['time'])
    elif row['action'] == 'start' and row['description'] == 'API_200':
        result_user[row['username']]['start'].append(row['time'])
    elif row['mqtt'] == 'foxlink/users/{}/move-rescue-station'.format(row['username']):
            result_user[row['username']]['rescue'] = True
    elif row['action'] == 'reject' and row['description'] == 'API_200':
        result_user[row['username']]['reject'].append(row['time'])
        
for index, row in table_audit.iterrows():
    if row['action'] == 'MISSION_ASSIGNED':
        result_user[row['user']]['assign'].append(row['created_date'])
        result_user[row['user']]['mission_id'].append(row['record_pk'])
        
for index, row in table_mission.iterrows():
    result_user[row['user']]['repair_start_date'].append(row['event_start_date'])
    result_user[row['user']]['repair_end_date'].append(row['event_end_date'])
    
for i in range(1, USER_NUMBER + 1):
    name = 'C0{}'.format(str(i).zfill(3))
    if i >= 1 and i <= 42:
        if result_user[name]['rescue'] and len(result_user[name]['start']) == 2:
            result_user[name]['is_correct'] = True
            period.append((result_user[name]['assign'][1] - result_user[name]['repair_end_date'][0]) / pd.Timedelta(seconds=1) - 60)
    elif i >= 43 and i <= 48:
        if len(result_user[name]['start']) == 2 and result_user[name]['rescue'] == False:
            result_user[name]['is_correct'] = True
            period.append((result_user[name]['assign'][1] - result_user[name]['repair_end_date'][0]) / pd.Timedelta(seconds=1))
    elif i >= 49 and i <= 84:
        if len(result_user[name]['start']) == 1 and result_user[name]['rescue'] == False:
            result_user[name]['is_correct'] = True
    elif i >= 85 and i <= 91:
        if len(result_user[name]['assign']) == 0:
            result_user[name]['is_correct'] = True

answer_user = pd.DataFrame.from_dict(result_user, orient='index').drop(columns=['rescue'], axis=1)
print('\n\n========== USER BASE ==========\n\n')
print(answer_user.to_string())

print('\n\n========== FINISH -> ASSIGNED AVG ==========')
print(sum(period) / len(period))

result_mission = {}

mission_id = table_mission['mission'].unique()
mission = {}
period = []


for m in mission_id:

    cursor = connection.cursor(buffered=True)

    mySql_insert_query = f"""SELECT created_date from foxlink.auditlogheaders a WHERE a.record_pk = '{m}' and a.`action` = 'MISSION_ASSIGNED'"""
    cursor.execute(mySql_insert_query)
    assign_date = cursor.fetchone()
    if assign_date:
        assign_date = pd.DataFrame(assign_date)[0][0]
    
    mySql_insert_query = f"""SELECT created_date from foxlink.auditlogheaders a WHERE a.record_pk = '{m}' and a.`action` = 'MISSION_ACCEPTED'"""
    cursor.execute(mySql_insert_query)
    accept_date = cursor.fetchone()
    if accept_date:
        accept_date = pd.DataFrame(accept_date)[0][0]

    cursor.close()
    
    mission[m] = {
        'assign_date': assign_date,
        'acept_date': accept_date,
        'is_accept': True if accept_date else False
    }

for index, row in table_mission.iterrows():
    result_mission[row['event_id']] = {
        'mission_id': row['mission'],
        'device': row['device'],
        'event_start_time': row['event_start_date'],
        'event_end_time': row['event_end_date'],
        'mission_created_date': row['created_date'],
        'assign': mission[row['mission']]['assign_date'],
        'assignee': row['user'],
        'is_accept': mission[row['mission']]['is_accept']
    }
    print(row['user'], (mission[row['mission']]['assign_date'] - row['created_date']) / pd.Timedelta(seconds=1))
    if mission[row['mission']]['is_accept']:
        period.append((mission[row['mission']]['assign_date'] - row['created_date']) / pd.Timedelta(seconds=1))

answer_mission = pd.DataFrame.from_dict(result_mission, orient='index')
print('\n\n========== MISSION BASE ==========\n\n')
print(answer_mission.to_string())

print('\n\n========== CREATED -> ASSIGN AVG ==========')
print(sum(period) / len(period))

cursor = connection.cursor()
mySql_insert_query = f"""SELECT * FROM foxlink.missions m WHERE repair_start_date IS NULL AND is_cancel = 0"""
cursor.execute(mySql_insert_query)
not_assign_mission = cursor.fetchall()

print('\n\n========== NOT ASSIGNED MISSIONS ==========')
print(pd.DataFrame(not_assign_mission)[1])