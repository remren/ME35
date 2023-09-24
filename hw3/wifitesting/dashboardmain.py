import network
import time
import ubinascii
import urequests as requests

import lsm6ds3
import joypad

station = network.WLAN(network.STA_IF)
station.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

ssid = 'Tufts_Wireless'
password = ''

station.connect(ssid, password)
while station.isconnected() == False:
    time.sleep(1)
    pass
print('Connection successful')
print(station.ifconfig())

USERNAME = "remren"

url = 'https://io.adafruit.com/api/v2/%s/feeds' % USERNAME
# REMOVE THIS IN YOUR NOTION UPLOAD
key = ""
# REMOVE THIS IN YOUR NOTION UPLOAD
headers = {'X-AIO-Key':key,'Content-Type':'application/json'}
reply = requests.get(url,headers=headers)
if reply.status_code == 200:
    reply = reply.json() #a JSON array of info
    keys = [x['key'] for x in reply]
    groups = [x['group']['name'] for x in reply]
    names = [x['name'] for x in reply]
    values = [x['last_value'] for x in reply]
    ids = [x['id'] for x in reply]
print(f"Available Keys:{keys}")

imu = lsm6ds3.LSM6DS3(i2c_slot=1, scl_pin=3, sda_pin=2)
imu.init_lsm6ds3()

joy = joypad.Joypad(i2c_slot=0, scl_pin=1, sda_pin=0)
joy.digital_setup()

def sendit(keys_index, data):
    axurl = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (USERNAME, keys[keys_index])
    to_send = {'value': data}
    try:
        reply = requests.post(axurl,headers=headers,json=to_send)
    finally:
        # Very important to have .close()! See: https://forum.micropython.org/viewtopic.php?f=16&t=3260
        # Add to end of an object that makes sockets
        reply.close()

BTN_CONST = [1 << 6, 1 << 2, 1 << 5, 1 << 1, 1 << 0, 1 << 16]
def sendloop():
    while True:
        print("send attempt")
        imu_data 	= imu.readaccel()
        x_axis		= joy.read_joystick(14)
        y_axis		= joy.read_joystick(15)
        buttons		= [not joy.digital_read() & btn for btn in BTN_CONST]
        for i in range(1, 4):
            print(f"imu_data[{i}]={imu_data[i - 1]}")
            sendit(i, imu_data[i - 1])
        for i in range(4, 8):
            print(f"button[{i - 4}]={buttons[i - 4]}")
            indicator = 0
            if (buttons[i-4]):
                indicator = 1
            sendit(i, indicator)
        print(f"x_axis={x_axis}")
        sendit(8, x_axis)
        print(f"y_axis={y_axis}")
        sendit(9, y_axis)
        print("all sent!")

try:
    sendloop()
except KeyboardInterrupt:
    print('Interrupted')
finally:
    print('All set! There will be a clear state now.')