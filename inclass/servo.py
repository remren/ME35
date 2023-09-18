import time
from machine import Pin

GP = 15

class servo():
    def __init__(self, gpio=GP, start = 1.5):
        self.gpio = gpio
        self.pin = Pin(gpio, Pin.OUT)
        self.pos = self.run(start)
        
    def run(self, pos):
        up = int(pos * 1000)
        down = int(1/50 * 1000000 - up)
        self.pin.on()
        time.sleep_us(up)
        self.pin.off()
        time.sleep_us(down)

fred = servo(GP)
for i in range(10):
    speed = 1+i/10.  # go from 1 msec to 2 msec in 0.1 msec intervals
    print(speed)
    for j in range(50):   #run for 1 sec
        fred.run(speed)