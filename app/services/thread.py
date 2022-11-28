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
from multiprocessing import Process
logging.basicConfig(level=logging.INFO)

# class WorkerThread(threading.Thread):
class WorkerThread(Process):
    def __init__(self, username, behavier):
        super(WorkerThread,self).__init__()
        self.logger = logging.getLogger(username)
        self.username = username
        self.behavier = behavier
        self.token = None
        self.mission_id = 0
        self.topic = None
        self.client = None

    def mqtt(self, action):

        def on_subscribe(client, userdata, flags, rc):
            pass
            # self.logger.warning(f"client subscribe = {self.username}")

        def on_message(client, userdata, msg):

            info = msg.payload.decode()
            topic = msg.topic
            self.mission_id = json.loads(info)['mission_id']
            retain = msg.retain

            self.logger.warn(f"on_message:{self.username} {self.mission_id} {retain}")

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
            self.client = None
        
        try:
            if self.client == None:
                self.client = mqtt_client.Client(self.username)
                self.client.connect(MQTT_BROKER, MQTT_PORT)
                self.client.subscribe(self.topic)
                self.client.on_message = on_message
                self.client.on_subscribe = on_subscribe
                self.client.loop_start()
        except:
            self.logger.warning(f"{self.username} can't connect mqtt")
        
    def run(self):
        i = 0
        while i < len(self.behavier):
            status = None
            action = self.behavier[i]['api']
            response_time = self.behavier[i]['response_time']
            timeout = 60 # seconds
            self.logger.info(f"action:{action} begin to with timeout({timeout})")
            if action == 'login':
                status, self.token = login(self.username,timeout,logger=self.logger)

            elif action == 'logout':
                status = logout(self.token,self.username,timeout=timeout,logger=self.logger)
               
            elif action in ['accept', 'reject']:
                self.topic = f'foxlink/users/{self.username}/missions'
                self.mqtt(action)
                
                while self.mission_id == 0:
                    self.logger.info(f"Waiting the MQTT message for action:{action}")
                    time.sleep(10)

                status = mission_action(self.token, self.mission_id, action, self.username,timeout=timeout,logger=self.logger)

            elif action == 'start' and self.behavier[i - 1]['api'] == 'start':
                self.topic = f'foxlink/users/{self.username}/move-rescue-station'
                self.mqtt(action)

                while self.mission_id == 0:
                    self.logger.info(f"Waiting the MQTT message for action:{action}")
                    time.sleep(5)

            elif action in ['start', 'finish']:
                status = mission_action(self.token, self.mission_id, action, self.username,timeout=timeout,logger=self.logger)

            self.logger.info(f"ended {action} with status:{status}")

            if status and status >= 200 and status <= 299:
                self.logger.info(f"action:{action} completed.")
                i += 1

            time.sleep(response_time)

        self.logger.info("completed all tasks, leaving")