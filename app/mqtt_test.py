# from pymysql import NULL
# from paho.mqtt import client as mqtt_client
# from datetime import datetime
# import time, json, uuid


# def on_connect(client, userdata, flags, rc):
#     pass
#     if rc == 0:
#         print("Connected to MQTT Broker")
#     else:
#         print("Failed to connect, return code %d\n", rc)


# def connect_mqtt(client_id) -> mqtt_client:
#     client = mqtt_client.Client(client_id)
#     client.on_connect = on_connect
#     client.connect('140.118.157.9', 1883)
#     return client

# def subscribe(client_id, username, action, response_time):
#     mission_id = None

#     def on_message(client, userdata, msg):
#         time.sleep(response_time)

#         nonlocal mission_id
#         info = msg.payload.decode()
#         topic = msg.topic
#         retain = msg.retain
#         print(retain)
#         print(topic)
#         print(username)
#         print(info)

#         mission_id = json.loads(info)['mission_id']
#         client.disconnect()

#     client = connect_mqtt(client_id)
#     client.subscribe([(f'foxlink/users/{username}/missions', 2)])
#     client.on_message = on_message
#     client.loop_forever()
#     return mission_id

# subscribe(str(uuid.uuid4()), 'C0087', 'hello', 1)

import random
break_ls = sorted([random.randint(0, 10) for _ in range(91)],reverse=True)
print(break_ls)