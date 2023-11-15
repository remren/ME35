import network
import time
import ubinascii
import urequests as requests
import accel_wifi

station = network.WLAN(network.STA_IF)
station.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

# print("Scanning...")
# for _ in range(2):
#     scan_result = station.scan()
#     for ap in scan_result:
#         print("SSID:%s BSSID:%s Channel:%d Strength:%d RSSI:%d Auth:%d "%(ap))
#     print()
#     time.sleep_ms(1000)

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
key = "" # deleted, is AIO KEY
headers = {'X-AIO-Key':key,'Content-Type':'application/json'}
reply = requests.get(url,headers=headers)
if reply.status_code == 200:
    reply = reply.json() #a JSON array of info
    keys = [x['key'] for x in reply]
    groups = [x['group']['name'] for x in reply]
    names = [x['name'] for x in reply]
    values = [x['last_value'] for x in reply]
    ids = [x['id'] for x in reply]
    
print(keys)
print(groups)
print(names)
print(values)
print(ids)

# print(keys[1])
# axurl = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (USERNAME, keys[1])
# data = {'value':-1}
# reply = requests.post(axurl,headers=headers,json=data)
# #you should probably check the reply.status
# reply = requests.get(axurl,headers=headers)
# print(keys)
# print(groups)
# print(names)
# print(values)
# print(ids)


# async def sendit(keys_index):
# #     data = accel.returnaccel()[keys_index]
#     while True:
#         axurl = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (USERNAME, keys[keys_index])
#         data = {'value': 1}
#         reply = requests.post(axurl,headers=headers,json=data)
#     await asyncio.sleep_ms(10)
# 
# async def main(duration):
#         print("running async main")
#         asyncio.create_task(test.readaccel())			# read task
#         asyncio.create_task(sendit(1))	# send stdin task
#         await asyncio.sleep(duration)		# sleeps for duration secs
#     
# def run(runtime):
#     try:
#         asyncio.run(main(runtime)) # runs everything for __ seconds
#     except KeyboardInterrupt:
#         print('Interrupted')
#     finally:
#         asyncio.new_event_loop()  
#         print('All set! There will be a clear state now.')
# run(999)

import uasyncio as asyncio
import lsm6ds3

test = lsm6ds3.LSM6DS3()
test.init_lsm6ds3()

def sendit(keys_index, accel_data):
    axurl = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (USERNAME, keys[keys_index])
    data = {'value': accel_data}
    try:
        reply = requests.post(axurl,headers=headers,json=data)
    finally:
        # Very important to have .close()! See: https://forum.micropython.org/viewtopic.php?f=16&t=3260
        # Add to end of an object that makes sockets
        reply.close()

def sendloop():
    while True:
        print("send attempt")
        data = test.readaccel()
        for i in range(1, 4):
            print(f"data[{i}]={data[i - 1]}")
            sendit(i, data[i - 1])
        print("sent!")
        time.sleep(1.0)
    
try:
    sendloop()
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()  
    print('All set! There will be a clear state now.')
    
