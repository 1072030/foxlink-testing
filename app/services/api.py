import logging
import time

import requests
import json
from passlib.context import CryptContext
from pymysql import NULL
from app.env import SERVER_URL
from app.services.log import create_log, kill_process
from datetime import datetime

ROUNDS = 10000
PWD_SCHEMA = "sha256_crypt"
PWD_SALT = "F0XL1NKPWDHaSH"
pwd_context = CryptContext(schemes=[PWD_SCHEMA], deprecated="auto")
PASSWORD = pwd_context.hash("foxlink", salt=PWD_SALT)


def login(username, id, timeout=60, logger=logging):
    global PASSWORD
    status = None
    token = None

    payloads = {
        'username': username,
        'password': PASSWORD,
        'client_id': id
    }

    try:
        r = requests.post(f'{SERVER_URL}/auth/token', data=payloads, timeout=timeout)
        token = r.json()['access_token']
        status = r.status_code
    except ConnectionResetError as e:
        time.sleep(5)
        logger.warning(f"can't login, connection reset.")
    except Exception as e:
        logger.warning(f"can't login, unknown exception occur.")
        logger.warning(e)

    create_log(
        param={
            'mission_id': NULL,
            'mqtt': '',
            'username': username,
            'action': 'login',
            'description': f'{status},{token}',
            'mqtt_detail': '',
            'time': datetime.utcnow(),
        }
    )

    time.sleep(2)

    return status, token


def logout(token, username, reason='OffWork', timeout=60, logger=logging):
    status = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }

    try:
        r = requests.post(f'{SERVER_URL}/users/get-off-work?reason={reason}', headers=header, timeout=timeout)
        status = r.status_code
    except ConnectionResetError as e:
        logger.warning(f"can't logout, connection reset.")
    except Exception as e:
        logger.warning(f"can't logout, exception occur.")
        logger.warning(e)

    create_log(
        param={
            'mission_id': NULL,
            'mqtt': '',
            'username': username,
            'action': 'logout',
            'description': f'{status}',
            'mqtt_detail': '',
            'time': datetime.utcnow(),
        }
    )

    time.sleep(2)

    return status


def mission_action(token, mission_id, action, username, timeout=60, logger=logging):
    status = None
    result = None
    header = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    try:
        if action == 'reject':
            r = requests.get(f'{SERVER_URL}/missions/{mission_id}/reject', headers=header, timeout=timeout)
        elif action == 'start':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/start', headers=header, timeout=timeout)
        elif action == 'accept':
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/accept', headers=header, timeout=timeout)
        elif action == "finish":
            r = requests.post(f'{SERVER_URL}/missions/{mission_id}/finish', headers=header, timeout=timeout)
        else:
            logger.warning(f"[mission action]unknown action: {action}")

        status = r.status_code

    except ConnectionResetError as e:
        logger.warning(f"can't perform action({action}), connection reset.")
    except Exception as e:
        logger.warning(f"can't perform action({action}), unknown exception occur.")
        logger.info(e)

    try:
        result = json.dumps(r.json())
    except Exception as e:
        logger.warning(f"can't dump result of action({action}), exception occur.")
        logger.info(e)

    create_log(
        param={
            'mission_id': mission_id,
            'mqtt': '',
            'username': username,
            'action': action,
            'description': f'API_{status}',
            'mqtt_detail': f'{result}',
            'time': datetime.utcnow(),
        }
    )
    time.sleep(2)

    return status


def set_shift_time(did, date1, date2, timeout=60, logger=logging):
    data = {
        'id': did + 1,
        "shift_beg_time": str(date1),
        "shift_end_time": str(date2)
    }
    try:
        r = requests.get(
            f'{SERVER_URL}/shift/update',
            params=data,
            timeout=timeout
        )
        return r.status_code
    except ConnectionResetError as e:
        logger.warning(f"can't update, connection reset.")
    except Exception as e:
        logger.warning(f"can't update, unknown exception occur.")
        logger.warning(e)
