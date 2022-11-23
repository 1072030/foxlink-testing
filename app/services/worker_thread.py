import threading, time, random, logging, json
from datetime import datetime, timedelta
from paho.mqtt import client as mqtt_client
from app.env import MQTT_BROKER, MQTT_PORT
from app.services.api import login, logout, mission_action
from app.services.log import create_log
from app.env import DAY_SHIFT_BEGIN, DAY_SHIFT_END, RESPONSE_START, RESPONSE_END


class WorkerThread(threading.Thread):
    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.username = None
        self.user_id = user_id + 1
        self.shift_type = None
        self.token = None
        self.mission_id = None
        self.client = None

    def get_shift_type(self):
        now = datetime.now() + timedelta(hours=8)
        day_begin = datetime.strptime(DAY_SHIFT_BEGIN, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        day_end = datetime.strptime(DAY_SHIFT_END, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

        if now < day_begin:
            return 1
        if now < day_end:
            return 0
        return 1

    def get_action(self):
        r = random.randint(1, 100)
        
        if r <= 90:
            return "accept"

        if r <= 95:
            return "reject"
        
        return None

    def get_response_time(self):
        return random.randint(RESPONSE_START, RESPONSE_END)
    
    def all_login_logout(self):
        self.username = 'C{}{}'.format(self.get_shift_type(), str(self.user_id).zfill(3))
        status, self.token = login(self.username, self.user_id)
        logout(self.token, self.username)
    
    def check_user_info(self):
        if self.shift_type != self.get_shift_type():
            while True:
                if self.token:
                    status = logout(self.token, self.username)
                    if status and status == 200:
                        break
                else:
                    break
            
            self.shift_type = self.get_shift_type()
            self.username = 'C{}{}'.format(self.get_shift_type(), str(self.user_id).zfill(3))
            self.topic_mission = f'foxlink/users/{self.username}/missions'
            self.topic_rescue = f'foxlink/users/{self.username}/move-rescue-station'
            self.token = None
            self.mission_id = None

            if self.client:
                self.client.loop_stop()
                self.mqtt()
            
        if not self.token:
             while True:
                status, self.token = login(self.username, self.user_id)
                if status and status == 200:
                    break

    def take_action(self, action):
        time.sleep(self.get_response_time())
        status = mission_action(self.token, self.mission_id, action, self.username)


    def mqtt(self):
        def on_message(client, userdata, msg):
            info = msg.payload.decode()
            topic = msg.topic
            mission_id = json.loads(info)['mission_id']
            
            is_diff_mission = True
            if self.mission_id == mission_id:
                is_diff_mission = False

            if is_diff_mission:
                self.mission_id = mission_id

                logging.warn(f"on_message:{self.username} {topic} {self.mission_id}")

                create_log(
                    param = {
                        'mission_id': self.mission_id,
                        'mqtt': topic,
                        'username': self.username,
                        'action': '',
                        'description': f'receive_mqtt',
                        'mqtt_detail': info,
                        'time': datetime.now(),
                    }
                )

                if topic == self.topic_mission:
                    action = self.get_action()
                    if action == "accept":
                        self.take_action("accept")
                        self.take_action("start")
                        self.take_action("finish")
                    elif action == "reject":
                        self.take_action("reject")
                    else:
                        create_log(
                            param = {
                                'mission_id': self.mission_id,
                                'mqtt': topic,
                                'username': self.username,
                                'action': 'no_action',
                                'description': f'receive_mqtt',
                                'mqtt_detail': info,
                                'time': datetime.now(),
                            }
                        )

                elif topic == self.topic_rescue:
                    self.take_action("start")
        
        try:
            self.client = mqtt_client.Client(self.username)
            self.client.connect(MQTT_BROKER, MQTT_PORT)
            self.client.subscribe([(self.topic_mission, 2), (self.topic_rescue, 2)])
            self.client.on_message = on_message
            self.client.loop_start()
        except:
            logging.warning(f"{self.username} can't connect mqtt")

    def run(self):
        while True:
            self.check_user_info()
            if self.client:
                self.client.loop_stop()
            self.mqtt()
            time.sleep(300)