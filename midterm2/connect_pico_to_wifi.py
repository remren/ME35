import network
import time
import ubinascii

def connect_wifi():
    ### CONNECT THE PICO TO WIFI ###
    station = network.WLAN(network.STA_IF)
    station.active(True)

    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)

    ssid = 'tufts_eecs'
    password = 'foundedin1852'

    station.connect(ssid, password)
    while station.isconnected() == False:
        time.sleep(1)
        pass
    print('Connection successful')
    print(station.ifconfig())
    ### DONE CONNECTING TO WIFI ###
