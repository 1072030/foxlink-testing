import logging
import time
from pymysql import NULL
import requests, json
from app.env import SERVER_URL
from app.services.log import create_log, kill_process
from datetime import datetime

def login(username, id,timeout=60,logger=logging):
    status = None
    token = None

    payloads = {
        'username': username,
        'password': 'foxlink',
        'client_id': id
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
        r = requests.post(f'{SERVER_URL}/auth/token',data=payloads, timeout=timeout)
        token = r.json()['access_token']
        status = r.status_code

    except Exception as e:
        logger.warning(f"can't login, exception occur.")
        logger.warning(e)

    return status, token

def logout(token, username, reason='OffWork',timeout=60,logger=logging):
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
        r = requests.post(f'{SERVER_URL}/users/get-off-work?reason={reason}', headers=header, timeout=timeout)
        status = r.status_code

    except Exception as e:
        logger.warning(f"can't logout, exception occur.")
        logger.warning(e)

    return status

def mission_action(token, mission_id, action, username,timeout=60,logger=logging):
    status = None
    result = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    try:
        if action == 'reject':
            r = requests.get(f'{SERVER_URL}/missions/{mission_id}/reject', headers=header,timeout=timeout)
        elif action == 'start':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/start', headers=header,timeout=timeout)
        elif action == 'accept':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/accept', headers=header,timeout=timeout)
        elif action == "finish":
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/finish', headers=header, timeout=timeout)
        else:
            logger.warning(f"[mission action]unknown action: {action}")

        status = r.status_code
        
    except Exception as e:
        logger.warning(f"can't perform action({action}), exception occur.")
        logger.info(e)

    try:
        result = json.dumps(r.json())

    except Exception as e:
        logger.warning(f"can't dump result of action({action}), exception occur.")
        logger.info(e)


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

   
    return status