import threading, time, random, logging, json
from datetime import datetime, timedelta
from paho.mqtt import client as mqtt_client
from app.env import MQTT_BROKER, MQTT_PORT, RESPONSE_START, RESPONSE_END
from pymysql import NULL
from app.services.api import login, logout, mission_action
from app.services.log import create_log
from app.services.api import set_shift_time

class WorkerThread(threading.Thread):
    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.username = None
        self.user_id = user_id
        self.shift_type = (self.get_shift_type() + 1) % 2
        self.token = None
        self.mission_id = None
        self.client = None
    
    def update_shift(self):
        hour = (datetime.now() + timedelta(hours=8)).hour
        
        if self.shift_type != self.get_shift_type():
            time1 = f'{(hour+1)%24}:00:00'
            time2 = f'{hour%24}:00:00'
            
            set_shift_time(self.shift_type, time1, time2)
            self.shift_type = self.get_shift_type()
            set_shift_time(self.shift_type, time2, time1)
            
            create_log(
                param = {
                    'mission_id': NULL,
                    'mqtt': '',
                    'username': self.username,
                    'action': '',
                    'description': f'shift',
                    'mqtt_detail': f'{self.shift_type}, beg: {time2}, end: {time1}',
                    'time': datetime.now(),
                }
            )
            
            fail_count = 0
            if self.token:
                while True:
                    is_success, fail_count = self.get_logout_status(logout(self.token, self.username), fail_count)
                    if is_success: break
                    
            self.token = None
            self.mission_id = None
            

    def get_shift_type(self):
        if datetime.now().hour % 2 == 0:
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
    
    def get_logout_status(self, status, fail_count):
        if status and status == 200:
            return True, 0
        
        fail_count += 1
        if fail_count == 10:
            return True, 0
        
        return False, fail_count
    
    def check_user_info(self):
        if not self.token:
            self.username = 'C{}{}'.format(self.get_shift_type(), str(self.user_id).zfill(3))
            self.topic_mission = f'foxlink/users/{self.user_id}/missions'
            self.topic_rescue = f'foxlink/users/{self.user_id}/move-rescue-station'
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
            self.update_shift()
            self.check_user_info()
            if self.client:
                self.client.loop_stop()
            self.mqtt()
            time.sleep(60)