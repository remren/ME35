import paho.mqtt.client as mqtt #import the client1
import time
import sys

def whenCalled(client, userdata, message):
    print("received " ,str(message.payload.decode("utf-8")))
    print("from topic ",message.topic)


# Client: Username -> Adafruit IO Username, Password -> Adafruit IO Key
username = "remren"
# REMOVE THIS IN YOUR UPLOAD
key = ""
broker = "io.adafruit.com"
topic_pub = f"{username}/feeds/current-color"

client = mqtt.Client("fred") # use a unique name
client.username_pw_set(username, key)

client.on_message = whenCalled # callback

try:
    client.connect(broker, port=8883)
except Exception as e:
    print("can't connect to mqtt server{}{}".format(type(e).__name__, e))
    while True:
        print("stop.")

print('Connected to %s MQTT broker' % broker)

client.loop_start() #start the loop
client.subscribe(f"{username}/feeds/current-color")

i = 0
while True:
    print("Publishing message to topic",topic_pub)
    client.publish(topic_pub,"iteration %d" % i)
    time.sleep(4) # wait for a little
    i+=1
#     client.publish(topic_pub % "/get", "HELP")
client.loop_stop() #stop the loop