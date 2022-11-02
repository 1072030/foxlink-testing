from app.env import MQTT_BROKER, MQTT_PORT
from paho.mqtt import client as mqtt_client
from app.services.log import create_log
from datetime import datetime
import time, json

def connect_mqtt(client_id) -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

def subscribe(client_id, username, action, response_time, topic):
    try:
        mission_id = None
        
        def on_message(client, userdata, msg):
            time.sleep(response_time)
            nonlocal mission_id
            info = msg.payload.decode()
            topic = msg.topic
            mission_id = json.loads(info)['mission_id']

            create_log(
                param = {
                    'mission_id': mission_id,
                    'mqtt': topic,
                    'username': username,
                    'action': action,
                    'description': 'receive_mqtt',
                    'mqtt_detail': info,
                    'time': datetime.now(),
                }
            )
            
            client.unsubscribe(topic)
            client.disconnect()

        client = connect_mqtt(client_id)
        client.subscribe(topic)
        client.on_message = on_message
        client.loop_forever()
        return mission_id
    except:
        return 0