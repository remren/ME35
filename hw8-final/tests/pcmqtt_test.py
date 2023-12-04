import paho.mqtt.client as mqtt

broker_address = "10.243.26.3"
client = mqtt.Client("arm")
client.connect(broker_address)
print('Connected to %s MQTT broker' % broker_address)
client.subscribe("arm")

def say_hello(name):
    client.publish("arm", name)
    print(f"message sent to mqtt:, {name}!")

say_hello("bob")