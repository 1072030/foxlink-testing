from datetime import datetime
import threading, time
from pymysql import NULL
from app.services.api import login, logout, mission_action
from app.services.log import create_log
from pymysql import NULL
from app.env import MQTT_BROKER, MQTT_PORT
from paho.mqtt import client as mqtt_client
from datetime import datetime
import time, json, logging

class WorkerThread(threading.Thread):
    def __init__(self, username, behavier):
        threading.Thread.__init__(self)
        self.username = username
        self.behavier = behavier
        self.token = None
        self.mission_id = 0
        self.topic = None
        self.client = None

    def mqtt(self, action):

        def on_subscribe(client, userdata, flags, rc):
            pass
            # logging.warning(f"client subscribe = {self.username}")

        def on_message(client, userdata, msg):

            info = msg.payload.decode()
            topic = msg.topic
            self.mission_id = json.loads(info)['mission_id']
            retain = msg.retain

            logging.warn(f"on_message:{self.username} {self.mission_id} {retain}")

            create_log(
                param = {
                    'mission_id': self.mission_id,
                    'mqtt': topic,
                    'username': self.username,
                    'action': action,
                    'description': f'receive_mqtt retain: {retain}',
                    'mqtt_detail': info,
                    'time': datetime.now(),
                }
            )
            
            self.client.unsubscribe(topic)
            self.client.disconnect()
            self.client.loop_stop()
        
        try:
            self.client = mqtt_client.Client(self.username)
            self.client.connect(MQTT_BROKER, MQTT_PORT)
            self.client.subscribe(self.topic)
            self.client.on_message = on_message
            self.client.on_subscribe = on_subscribe
            self.client.loop_start()
        except:
            logging.warning(f"{self.username} can't connect mqtt")
        
    def run(self):
        i = 0
        while i < len(self.behavier):
            status = None
            if self.behavier[i]['api'] == 'login':
                time.sleep(self.behavier[i]['response_time'])
                status, self.token = login(self.username)

            elif self.behavier[i]['api'] == 'logout':
                time.sleep(self.behavier[i]['response_time'])
                status = logout(self.token, self.username)

            elif self.behavier[i]['api'] == 'accept' or self.behavier[i]['api'] == 'reject':
                self.topic = f'foxlink/users/{self.username}/missions'
                self.mqtt(self.behavier[i]['api'])
                time.sleep(1)
                
                if self.mission_id != 0:
                    status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)

            elif self.behavier[i]['api'] == 'start':
                time.sleep(self.behavier[i]['response_time'])
                if self.behavier[i -1]['api'] == 'start':
                    self.topic = f'foxlink/users/{self.username}/move-rescue-station'
                    self.mqtt(self.behavier[i]['api'])
                    time.sleep(1)
                    if self.mission_id != 0:
                        status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)
                else:
                    status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)

            # create_log(
            #     param = {
            #         'mission_id': NULL,
            #         'mqtt': '',
            #         'username': self.username,
            #         'action': self.behavier[i]['api'],
            #         'description': f'{i} {status}',
            #         'mqtt_detail': '',
            #         'time': datetime.now(),
            #     }
            # )

            if status and status >= 200 and status <= 299:
                i += 1
            else:
                if self.client:
                    self.client.loop_stop()
                time.sleep(10)