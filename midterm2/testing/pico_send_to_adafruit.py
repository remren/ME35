import mqtt
import time
import connect_pico_to_wifi as wifi_helper

wifi_helper.connect_wifi()

# Adafruit IO MQTT sever has a rate limit of 30 req. per min, so 1 request every 2 seconds.
# Primarily from Chris Roger's "catchup" example

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    
# Client: Username -> Adafruit IO Username, Password -> Adafruit IO Key
user = "remren"
# REMOVE THIS IN YOUR UPLOAD
key  = ''

url = "io.adafruit.com"

# Initialize mqtt client
aio_client = mqtt.MQTTClient('test', server=url, port=8883, user=user, password=key)
aio_client.connect()

aio_client.set_callback(whenCalled)

# aio_client.subscribe(f'{username}/errors')

def send_temp():
    client.publish(f"{username}/feeds/currentftemp", 420)
# client.on_message = callback
# client.subscribe(f'{username}/errors')