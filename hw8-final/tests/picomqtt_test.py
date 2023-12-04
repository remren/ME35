import time
import machine
import mqtt
import network, ubinascii

def connect_wifi():
    ### CONNECT THE PICO TO WIFI ###
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
    print('Wi-Fi Connection Successful')
    print(station.ifconfig())
    ### DONE CONNECTING TO WIFI ###

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    led.on()
    time.sleep(0.5)
    led.off()
    
mqtt_thread = "arm"
    
def main():
    try:
        fred = mqtt.MQTTClient("device", '10.243.26.3', keepalive=600)
        print('Connected')
        fred.connect()
        fred.set_callback(whenCalled)
    except OSError as e:
        print('Failed')
        return
    
    fred.subscribe(mqtt_thread)
    try:
        while True:
            fred.check_msg() #check subscriptions - you might want to do this more often
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        fred.disconnect()
        print('done')
        
connect_wifi()
led = machine.Pin('LED', machine.Pin.OUT)
    
main()