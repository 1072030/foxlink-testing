import json, os

CURRENT_PATH = os.getcwd()
SCENARIO = 'test.json'

with open(f'{CURRENT_PATH}/app/scenario/{SCENARIO}') as jsonfile:
    testLogining_data = json.load(jsonfile)
    jsonfile.close()

THREAD_NUMBER = len(testLogining_data['worker_behavier'])
WORKER = testLogining_data['worker_behavier']
FOXLINK_EVENT = testLogining_data['foxlinkEvent']
DATABASE_HOST = 'mysql'
DATABASE_PORT = '3306'
DATABASE_USER = 'root'
DATABASE_PASSWORD = '123456'
DATABASE_NAME = 'foxlink'
MQTT_BROKER = '140.118.157.9'
MQTT_PORT = 1883
SERVER_URL = "http://140.118.157.9:8080"
TESTING_LOG = True

DAY_SHIFT_BEGIN = '07:40'
DAY_SHIFT_END = '20:00'
RESPONSE_START = 5
RESPONSE_END = 60
REPAIR_START = 5
REPAIR_END = 240