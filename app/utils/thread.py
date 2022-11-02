from datetime import datetime
import threading, uuid, time
from app.services.log import create_log
from pymysql import NULL
from app.mqtt.mqtt_main import subscribe
from app.services.api import login, logout, mission_action
from app.services.log import create_log
from app.env import RETRY

class WorkerThread(threading.Thread):
    def __init__(self, username, behavier):
        threading.Thread.__init__(self)
        self.username = username
        self.behavier = behavier
        self.token = None
        self.mission_id = 0

    def run(self):
        i = 0
        while i < len(self.behavier):
            status = None
            if self.behavier[i]['api'] == 'login':
                time.sleep(self.behavier[i]['response_time'])
                create_log(
                    param = {
                        'mission_id': NULL,
                        'mqtt': '',
                        'username': self.username,
                        'action': 'login',
                        'description': '',
                        'mqtt_detail': '',
                        'time': datetime.now(),
                    }
                )
                status, self.token = login(self.username)

            elif self.behavier[i]['api'] == 'logout':
                time.sleep(self.behavier[i]['response_time'])
                create_log(
                    param = {
                        'mission_id': NULL,
                        'mqtt': '',
                        'username': self.username,
                        'action': 'logout',
                        'description': '',
                        'mqtt_detail': '',
                        'time': datetime.now(),
                    }
                )
                status = logout(self.token, self.username)

            elif self.behavier[i]['api'] == 'accept' or self.behavier[i]['api'] == 'reject':
                new_mission_id = subscribe(str(uuid.uuid4()), self.username, self.behavier[i]['api'], self.behavier[i]['response_time'], f'foxlink/users/{self.username}/missions')

                if RETRY:
                    self.mission_id = new_mission_id
                    status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)
                else:
                    if new_mission_id == self.mission_id:
                        i -= 1
                    else:
                        self.mission_id = new_mission_id
                        status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)
            
            elif self.behavier[i]['api'] == 'start':
                time.sleep(self.behavier[i]['response_time'])
                if self.behavier[i -1]['api'] == 'start':
                    new_mission_id = subscribe(str(uuid.uuid4()), self.username, self.behavier[i]['api'], self.behavier[i]['response_time'], f'foxlink/users/{self.username}/move-rescue-station')
                    if RETRY:
                        self.mission_id = new_mission_id
                        status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)
                    else:
                        if new_mission_id == self.mission_id:
                            i -= 1
                        else:
                            self.mission_id = new_mission_id
                            status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)
                else:
                    status = mission_action(self.token, self.mission_id, self.behavier[i]['api'], self.username)

            if RETRY:
                if status and status < 400:
                    i += 1
            else:
                i += 1