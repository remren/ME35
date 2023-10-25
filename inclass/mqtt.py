import paho.mqtt.client as mqtt
import time

broker_address='10.243.83.152'

def callback(source,user,message):
    print(message.payload.decode())
    
client = mqtt.Client("Remy Gallard") 
client.on_message = callback

client.connect(broker_address)
client.loop_start()
client.subscribe('test')

for i in range(10):
    client.publish("test","hi: %d" % i)
    time.sleep(3)

client.loop_stop()
client.disconnect()