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
            'action': "mqtt:subscribe",
            'description': f'status:{rc}',
            'mqtt_detail': f'{userdata}',
            'time': datetime.now()
        }
    )


def on_message(client, userdata, msg):
    global topic_results, is_connect
    duplicate = False
    info = msg.payload.decode()
    topic = msg.topic
    retain = msg.retain
    mission_id = json.loads(info)['mission_id']

    logger.warn(f"on_message:{username} {mission_id} {retain}")

    if (
        retain or
        (
            topic in topic_results and
            len(topic_results[topic]) > 0 and
            mission_id == topic_results[topic][-1]
        )
    ):
        duplicate = True
    else:
        topic_results[topic].append(mission_id)

    create_log(
        param={
            'mission_id': mission_id,
            'mqtt': topic,
            'username': username,
            'action': "mqtt:receive",
            'description': f"retain: {retain}, duplicate: {duplicate}",
            'mqtt_detail': f"userdata:{userdata}\n, msg:{msg}",
            'time': datetime.now()
        }
    )


def on_connect(c, userdata, flags, rc):
    global is_connect, username, topic_results, client
    if (rc == 0):
        logger.info(f"Connection successful: Broker")
        for topic in topic_results.keys():
            client.subscribe(topic, 2)
        is_connect = True
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
            'action': "mqtt:connect",
            'description': f'{"success" if rc == 0 else "failed" }. status:{rc}',
            'mqtt_detail': f"{userdata}",
            'time': datetime.now()
        }
    )


def on_disconnect(client, userdata, rc):
    global topic_results, is_connect
    if rc == 0:
        logger.info("Disconnect successful")
    else:
        logger.error("Disconnect - unknown error.")
    create_log(
        param={
            'mission_id': NULL,
            'mqtt': "",
            'username': username,
            'action': "mqtt:disconnect",
            'description': f'{"success" if rc == 0 else "failed" }. status:{rc}',
            'mqtt_detail': f"{userdata}",
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
            'action': "subscribe",
            'description': f'@{topic}',
            'mqtt_detail': "",
            'time': datetime.now()
        }
    )


def mqtt_get(action, topic):
    global client, topic_results, is_connect

    while (not is_connect):
        # logger.info(f"for action:{action} waiting for mqtt to connect({is_connect})....")
        time.sleep(1)

    if (not topic in topic_results.keys()):
        register_topic(topic)

    while (len(topic_results[topic]) == 0):
        # logger.info(f"waiting for mqtt message with action:{action}")
        time.sleep(3)

    # result = topic_results[topic].pop(0)
    result = topic_results[topic][0]

    create_log(
        param={
            'mission_id': result,
            'mqtt': f'{topic}',
            'username': username,
            'action': action,
            'description': f'get from mqtt.',
            'mqtt_detail': f'',
            'time': datetime.now()
        }
    )

    return result


def mqtt_sync(status, topic):
    global topic_results
    if (status and status >= 200 and status <= 299):
        topic_results[topic].pop(0)


client = None
topic_results = {}
is_connect = False
username = "Unspecified"


def worker(_username, _behavier, _id, speed=1):
    # if (not _username == "C0001"):
    #     return
    global client, topic_results, is_connect, username, logger

    logger = logging.getLogger(_username)
    username = _username
    behavier = _behavier
    mission_id = 0
    worker_uuid = _id + 10000

    token = None

    ##### Start MQTT Client ######
    client = mqtt_client.Client(f"{username}#{worker_uuid}", clean_session=False)
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=10)
    client.loop_start()

    register_topic(f'foxlink/users/{worker_uuid}/move-rescue-station')
    register_topic(f'foxlink/users/{worker_uuid}/missions')

    i = 0
    j = 0
    while i < len(behavier):
        status = None
        action = behavier[i]['api']
        response_time = behavier[i]['response_time']
        timeout = 30  # seconds

        logger.info(f"action:{action} begin to with timeout({timeout})")

        time.sleep(float(response_time) / speed)

        if action == 'login':
            status, token = login(username, worker_uuid, timeout)

        elif action == 'logout':
            status = logout(token, username, timeout=timeout)

        elif action in ['accept', 'reject']:
            topic = f'foxlink/users/{worker_uuid}/missions'
            mission_id = mqtt_get(action, topic)
            status = mission_action(
                token,
                mission_id,
                action,
                username,
                timeout=timeout
            )
            mqtt_sync(status, topic)

        elif action == 'start' and behavier[i - 1]['api'] == 'finish':
            topic = f'foxlink/users/{worker_uuid}/move-rescue-station'
            mission_id = mqtt_get(action, topic)
            status = mission_action(
                token,
                mission_id,
                action,
                username,
                timeout=timeout
            )
            mqtt_sync(status, topic)

        elif action in ['start', 'finish']:
            status = mission_action(token, mission_id, action, username, timeout=timeout)

        logger.info(f"ended {action} with status:{status}")

        if status and 200 <= status and status <= 299:
            logger.info(f"action:{action} completed.")
            i += 1
            j = 0
        elif (status and 400 <= status <= 499):
            j += 1
            if (j > 10):
                i += 1
                j = 0
                if (action == "finish"):
                    mqtt_sync(200, f'foxlink/users/{worker_uuid}/missions')
                create_log(
                    param={
                        'mission_id': NULL,
                        'mqtt': '',
                        'username': username,
                        'action': action,
                        'description': f'skipping for error exceed',
                        'mqtt_detail': f'',
                        'time': datetime.now()
                    }
                )

    logger.info("completed all tasks, leaving")

    client.disconnect()

    return
