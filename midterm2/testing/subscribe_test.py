import paho.mqtt.subscribe as subscribe

username = "remren"
key = ""
auth = {'username':username,'password':key}

msg = subscribe.simple(f"{username}/errors", hostname="io.adafruit.com", port=8883, auth=auth)
print("%s %s" % (msg.topic, msg.payload))