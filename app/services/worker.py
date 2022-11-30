from datetime import datetime
import threading
import time
from pymysql import NULL
from app.services.api import login, logout, mission_action
from app.services.log import create_log
from pymysql import NULL
from app.env import MQTT_BROKER, MQTT_PORT
from paho.mqtt import client as mqtt_client
from datetime import datetime
import time
import json
import logging
from multiprocessing import Process
import asyncio
logging.basicConfig(level=logging.INFO)
logger = None

# class WorkerThread(threading.Thread):


def on_subscribe(client, userdata, flags, rc):
    global username

    logger.warning(f"client subscribe = {username}")

    create_log(
        param={
            'mission_id': NULL,
            'mqtt': '',
            'username': username,
            'action': "",
            'description': f'subscribe',
            'mqtt_detail': f'{repr(userdata)}',
            'time': datetime.now()
        }
    )


def on_message(client, userdata, msg):
    global topic_results, is_connect
    info = msg.payload.decode()
    topic = msg.topic
    retain = msg.retain
    mission_id = json.loads(info)['mission_id']

    logger.warn(f"on_message:{username} {mission_id} {retain}")

    topic_results[topic].append(mission_id)

    create_log(
        param={
            'mission_id': mission_id,
            'mqtt': topic,
            'username': username,
            'action': "",
            'description': f'mqtt receive (retain: {retain})',
            'mqtt_detail': info,
            'time': datetime.now()
        }
    )


def on_connect(c, user_data, flags, rc):
    global is_connect, username
    if (rc == 0):
        logger.info(f"Connection successful: Broker")
        create_log(
            param={
                'mission_id': NULL,
                'mqtt': "",
                'username': username,
                'action': "",
                'description': f'mqtt connected',
                'mqtt_detail': "",
                'time': datetime.now()
            }
        )
        is_connect = True
        return
    elif (rc == 1):
        logger.warn("Connection refused - incorrect protocol version")
    elif (rc == 2):
        logger.warn("Connection refused - invalid client identifier")
    elif (rc == 3):
        logger.warn("Connection refused - server unavailable")
    elif (rc == 4):
        logger.warn("Connection refused - bad username or password")
    elif (rc == 5):
        logger.warn("Connection refused - not authorised")
    else:
        logger.error("Connection refused - unknown error.")
    create_log(
        param={
            'mission_id': NULL,
            'mqtt': "",
            'username': username,
            'action': "",
            'description': f'mqtt connection failed',
            'mqtt_detail': "",
            'time': datetime.now()
        }
    )


def on_disconnect(client, userdata, rc):
    global topic_results, is_connect
    if rc == 0:
        logger.info("Disconnect successful")
        create_log(
            param={
                'mission_id': NULL,
                'mqtt': "",
                'username': username,
                'action': "",
                'description': f'mqtt disconnected by user.',
                'mqtt_detail': "",
                'time': datetime.now()
            }
        )
    else:
        logger.error("Disconnect - unknown error.")
        create_log(
            param={
                'mission_id': NULL,
                'mqtt': "",
                'username': username,
                'action': "",
                'description': f'mqtt disconnected',
                'mqtt_detail': "",
                'time': datetime.now()
            }
        )
    is_connect = False


def register_topic(topic):
    global client, topic_results, is_connect
    logger.info(f"{topic} registered")
    topic_results[topic] = []
    client.subscribe(topic, 2)
    create_log(
        param={
            'mission_id': NULL,
            'mqtt': "",
            'username': username,
            'action': "",
            'description': f'try subscribe: {topic}',
            'mqtt_detail': "",
            'time': datetime.now()
        }
    )


def mqtt(action, topic):
    global client, topic_results, is_connect

    while (not is_connect):
        # logger.info(f"for action:{action} waiting for mqtt to connect({is_connect})....")
        time.sleep(1)

    if (not topic in topic_results.keys()):
        register_topic(topic)

    while (len(topic_results[topic]) == 0):
        # logger.info(f"waiting for mqtt message with action:{action}")
        time.sleep(3)

    result = topic_results[topic].pop(0)

    create_log(
        param={
            'mission_id': NULL,
            'mqtt': f'{topic}',
            'username': username,
            'action': action,
            'description': f'retrieving',
            'mqtt_detail': f'result:{result}',
            'time': datetime.now()
        }
    )

    return result


client = None
topic_results = {}
is_connect = False
username = "Unspecified"


def worker(_username, _behavier, _id, speed=1):
    global client, topic_results, is_connect, username, logger

    logger = logging.getLogger(_username)
    username = _username
    behavier = _behavier
    mission_id = 0
    id = _id + 10000

    token = None

    ##### Start MQTT Client ######
    client = mqtt_client.Client(f"{username}#{_id}")
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    i = 0
    fetch = True

    while i < len(behavier):
        status = None
        action = behavier[i]['api']
        response_time = behavier[i]['response_time']
        timeout = 30  # seconds

        logger.info(f"action:{action} begin to with timeout({timeout})")

        time.sleep(float(response_time) / speed)

        if action == 'login':
            status, token = login(username, id, timeout)

        elif action == 'logout':
            status = logout(token, username, timeout=timeout)

        elif action in ['accept', 'reject']:
            if (fetch):
                mission_id = mqtt(action, f'foxlink/users/{id}/missions')

            status = mission_action(
                token,
                mission_id,
                action,
                username,
                timeout=timeout
            )
        elif action == 'start' and behavier[i - 1]['api'] == 'finish':
            if (fetch):
                mission_id = mqtt(action, f'foxlink/users/{id}/move-rescue-station')
            status = mission_action(token, mission_id, action, username, timeout=timeout)

        elif action in ['start', 'finish']:
            status = mission_action(token, mission_id, action, username, timeout=timeout)

        logger.info(f"ended {action} with status:{status}")

        if status and status >= 200 and status <= 299:
            logger.info(f"action:{action} completed.")
            fetch = True
            i += 1
        else:
            fetch = False

    logger.info("completed all tasks, leaving")

    client.disconnect()

    return
