import mqtt
import time
# import connect_pico_to_wifi as wifi_helper # DEBUG

# wifi_helper.connect_wifi() # DEBUG

# Adafruit IO MQTT sever has a rate limit of 30 req. per min, so 1 request every 2 seconds.
# Primarily from Chris Roger's "catchup" example

# Memory issues? https://github.com/orgs/micropython/discussions/11559

class mqttAIO:
    def __init__(self):
        # Client: Username -> Adafruit IO Username, Password -> Adafruit IO Key
        self.user = "remren"
        # REMOVE THIS IN YOUR UPLOAD
        key  = ''

        url = "io.adafruit.com"

        # Initialize mqtt client
        self.aio_client = mqtt.MQTTClient('test', server=url, user=self.user, password=key)
        self.aio_client.connect()
#         self.aio_client.set_callback(self.whenCalled)
    
#     def whenCalled(self, topic, msg):
#         print((topic.decode(), msg.decode()))

# Sends both temps to Adafruit. Only distinguishes for the Pico's display, not here.
    def send_temp(self, tempF, tempC):
        self.aio_client.publish(f"{self.user}/f/currentftemp", str(tempF))
        self.aio_client.publish(f"{self.user}/f/currentctemp", str(tempC))
