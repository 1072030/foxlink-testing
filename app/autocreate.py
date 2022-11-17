import logging, time
import pandas as pd
from datetime import datetime
from app.utils.query_db import query_server, query_local
from app.services.mission_thread import MissionThread
from pymysql import NULL

def get_device():
    sql = f"""SELECT project , line , device_name  from foxlink.devices d WHERE workshop = 1 and project != 'rescue' """
    data = query_server(sql)
    
    device = pd.DataFrame(data)
    device.rename(columns={0:'project', 1:'line', 2:'device_name'}, inplace=True)

    return device


if __name__ == '__main__':
    device = get_device()
    THREAD_NUMBER = len(device)
    mission_thread = []

    for i in range(THREAD_NUMBER):
        print(device['project'][i], device['line'][i], device['device_name'][i])
        mission_thread.append(MissionThread(device['project'][i], device['line'][i], device['device_name'][i]))
        mission_thread[i].start()
    
    for i in range(THREAD_NUMBER):
        mission_thread[i].join()