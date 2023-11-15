import connect_pico_to_wifi as wifi_helper
import time
import urequests as requests

wifi_helper.connect_wifi()

USERNAME = "remren"

url = 'https://io.adafruit.com/api/v2/%s/feeds' % USERNAME
# REMOVE THIS IN YOUR NOTION UPLOAD
# key = None
key = ""
# REMOVE THIS IN YOUR NOTION UPLOAD
headers = {'X-AIO-Key':key,'Content-Type':'application/json'}
# reply = requests.get(url,headers=headers)
# if reply.status_code == 200:
#     reply = reply.json() #a JSON array of info
#     keys = [x['key'] for x in reply]
#     groups = [x['group']['name'] for x in reply]
#     names = [x['name'] for x in reply]
#     values = [x['last_value'] for x in reply]
#     ids = [x['id'] for x in reply]
# print(f"Available Keys:{keys}")

# imu = lsm6ds3.LSM6DS3(i2c_slot=1, scl_pin=3, sda_pin=2)
# imu.init_lsm6ds3()
# 
# joy = joypad.Joypad(i2c_slot=0, scl_pin=1, sda_pin=0)
# joy.digital_setup()
# 
def sendit(key_name, data):
    axurl = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (USERNAME, key_name)
    to_send = {'value': data}
    try:
        reply = requests.post(axurl,headers=headers,json=to_send)
    finally:
        # Very important to have .close()! See: https://forum.micropython.org/viewtopic.php?f=16&t=3260
        # Add to end of an object that makes sockets
        reply.close()
        
sendit("currentftemp", 69)
print("done!")


