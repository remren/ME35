# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

# To connect to the Adafruit mqtt broker.

import paho.mqtt.client as mqtt
import random
import time

broker = 'io.adafruit.com'
port   = 8883
topic  = "feeds/current_color"
username = "remren"
password = ""
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failure to connect. return code={rc}")

def connect_mqtt():      
    # Set connecting client ID
    client = mqtt.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break
        
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()
    
run()