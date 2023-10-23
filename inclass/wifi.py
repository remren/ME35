import network
import time
import ubinascii

station = network.WLAN(network.STA_IF)
station.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

print("Scanning...")
for _ in range(2):
    scan_result = station.scan()
    for ap in scan_result:
        print("SSID:%s BSSID:%s Channel:%d Strength:%d RSSI:%d Auth:%d "%(ap))
    print()
    time.sleep_ms(1000)
    
    
ssid = 'Tufts_Wireless'
password = ''

station.connect(ssid, password)
while station.isconnected() == False:
    time.sleep(1)
    pass
print('Connection successful')
print(station.ifconfig())

# import urequests as requests
# 
# url = "https://worldtimeapi.org/api/timezone/America/New_York"
# reply = requests.get(url)
# print(reply)

import urequests as requests

reply = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")
print(reply.json()['datetime'] if reply.status_code == 200 else 'Error')
