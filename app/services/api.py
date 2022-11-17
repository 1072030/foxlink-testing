import logging
import time
from pymysql import NULL
import requests, json
from app.env import SERVER_URL, SCENARIO
from app.services.log import create_log, kill_process
from datetime import datetime

def login(username, id):
    status = None
    payloads = {
        'username': username,
        'password': 'foxlink',
        # 'client_id': id
    }

    create_log(
        param = {
            'mission_id': NULL,
            'mqtt': '',
            'username': username,
            'action': 'login',
            'description': '',
            'mqtt_detail': '',
            'time': datetime.now(),
        }
    )

    try:
        r = requests.post(f'{SERVER_URL}/auth/token',data=payloads, timeout=120)
        token = r.json()['access_token']
        status = r.status_code
    except Exception as e:
        logging.warning(f"{username} can't login")
        logging.warning(e)
        token = None
    return status, token

def logout(token, username, reason='OffWork'):
    status = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }

    create_log(
        param = {
            'mission_id': NULL,
            'mqtt': '',
            'username': username,
            'action': 'logout',
            'description': '',
            'mqtt_detail': '',
            'time': datetime.now(),
        }
    )

    try:
        r = requests.post(f'{SERVER_URL}/users/get-off-work?reason={reason}', headers=header, timeout=120)
        status = r.status_code
    except Exception as e:
        logging.warning(f"{username} can't logout")
        logging.warning(e)
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
        elif action == 'finish':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/finish', headers=header)
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

    if status == 200 and action == 'start' and SCENARIO == "test3.json":
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
                    time.sleep(30)
                else:
                    break
            except:
                logging.warning(f"{username} can't finish")
                result = None

    return status