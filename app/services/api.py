import logging
import time
from pymysql import NULL
import requests, json
from app.env import SERVER_URL
from app.services.log import create_log
from datetime import datetime

def login(username):
    status = None
    payloads = {
        'username': username,
        'password': 'foxlink'
    }
    try:
        r = requests.post(f'{SERVER_URL}/auth/token',data=payloads)
        token = r.json()['access_token']
        status = r.status_code
    except:
        logging.warning(f"{username} can't login")
        token = None
    return status, token

def logout(token, username, reason='OffWork'):
    status = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    try:
        r = requests.post(f'{SERVER_URL}/users/get-off-work?reason={reason}', headers=header)
        status = r.status_code
    except:
        logging.warning(f"{username} can't logout")
    return status

def mission_action(token, mission_id, action, username):
    status = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    try:
        if action == 'reject':
            r = requests.get(f'{SERVER_URL}/missions/{mission_id}/reject', headers=header)
        elif action == 'start':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/start', headers=header)
        elif action == 'accept':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/accept', headers=header)
        status = r.status_code
    except:
        logging.warning(f"{username} can't {action}")

    try:
        result = json.dumps(r.json())
    except:
        logging.warning(f"{username} can't dumps {action}")
        result = None

    create_log(
        param = {
            'mission_id': mission_id,
            'mqtt': '',
            'username': username,
            'action': action,
            'description': f'API_{status}',
            'mqtt_detail': f'{result}',
            'time': datetime.now(),
        }
    )

    if status == 200 and action == 'start':
        while True:
            try:
                f = requests.post(f'{SERVER_URL}/missions/{mission_id}/finish', headers=header)
                result = json.dumps(f.json())
                create_log(
                    param = {
                        'mission_id': mission_id,
                        'mqtt': '',
                        'username': username,
                        'action': 'finish',
                        'description': f'API_{f.status_code}',
                        'mqtt_detail': f'{result}',
                        'time': datetime.now(),
                    }
                )
                if f.status_code != 200:
                    time.sleep(15)
                else:
                    break
            except:
                logging.warning(f"{username} can't finish")
                result = None

    return status