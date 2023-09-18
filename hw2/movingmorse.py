import uasyncio as asyncio
import time

import lsm6ds3

unit = lsm6ds3.LSM6DS3
unit.init_lsm6ds3()

class MovingMorse:
    def __init__(self):
        print("test")
        self.gyro = []
        self.prev = []
        self.axis = 2
        
        self.last_was = 1
        
        self.gyro = unit.readgyro()[self.axis]
        self.prev = self.gyro
        
        self.sum  = 0
        while True:
            self.gyro = unit.readaccel()[self.axis]
            diff = self.prev - self.gyro
            if diff > 500 and self.last_was == 0:
                print("up")
                self.last_was = 1
            if diff < -500 and self.last_was == 1:
                print("down")
                self.last_was = 0
#             print(diff)
            self.prev = self.gyro
#             print(diff)
            print(self.sum)
            self.sum = self.sum + self.gyro
            time.sleep(0.2)
    
test = MovingMorse()
    