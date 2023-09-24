# https://www.pololu.com/file/0J1087/LSM6DS33.pdf
# https://github.com/jposada202020/MicroPython_LSM6DSOX/blob/master/micropython_lsm6dsox/lsm6dsox.py
# From Chris Roger's ME35 Page!

from machine import Pin, I2C
import struct, time

LSM = 0x6A
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
print(f"I2C Devices Scanned: {[hex(i) for i in i2c.scan()]}")

class LSM6DS3:
    def __init__(self):
        self.gyro = []
        self.accel = []
    
    def init_lsm6ds3(self):
        ID = i2c.readfrom_mem(LSM, 0x0F, 1)
        time.sleep(0.2)
        ID = struct.unpack('<b',ID)[0]

        rate = {'done': 0b0000,'12.5':0b0001,'26':0b0010,'52':0b0011,'104':0b0100,'208':0b0101,'416':0b0110,'833':0b0111,'1.66k':0b1000,'3.33k':0b1001,'6.66k':0b1010,'1.6':0b1011}
        anti_alias = {'400':0b00,'200':0b01,'100': 0b10, '50':0b11}
        XL_range = {'2g':0b00,'4g':0b10,'8g':0b11, '16g':0b01}
        G_range = {'250':0b00, '500':0b01,'1000':0b10,'2000':0b11}
        G_125_fullscale = 0

        XLfactor = (0.061, 0.488, 0.122, 0.244)
        Gfactor = (8.75, 17.50, 35.0, 70.0)

        # 58 = =high performance, +/- 4g
        XL = (rate['208']<<4) + (XL_range['4g']<<2) + anti_alias['400']
        i2c.writeto_mem(LSM, 0x10, struct.pack('>b',XL)) # enable accel

        # 58 = high performance - 1000 dps
        G = (rate['1.66k']<<4) + (G_range['1000']<<2) + (G_125_fullscale <<1) + 0
        i2c.writeto_mem(LSM, 0x11, struct.pack('>b',G)) # enable gyro

        time.sleep(0.2)

        temp = i2c.readfrom_mem(LSM, 0x20, 2)
        temp = struct.unpack('<h',temp)[0]
        temp /256 + 25.0 # what's the purpose of this?

        gyro = i2c.readfrom_mem(LSM, 0x22, 6)
        gyro = struct.unpack('<hhh',gyro)

        accel = i2c.readfrom_mem(LSM, 0x28, 6)
        accel = struct.unpack('<hhh',accel)
        
    def readaccel(self):
        print("entered read accel!")
        self.accel = i2c.readfrom_mem(LSM, 0x28, 6)
        self.accel = struct.unpack('<hhh',self.accel)
        print(self.accel)
        return self.accel
    
    def readgyro(self):
        self.gyro = i2c.readfrom_mem(LSM, 0x22, 6)
        self.gyro = struct.unpack('<hhh',self.gyro)
        print(self.gyro)
        return self.gyro
    
test = LSM6DS3()
test.init_lsm6ds3()
test.readaccel()