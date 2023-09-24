#https://www.pololu.com/file/0J1087/LSM6DS33.pdf
#https://github.com/jposada202020/MicroPython_LSM6DSOX/blob/master/micropython_lsm6dsox/lsm6dsox.py
# From Chris Roger's ME35 Page!

from machine import Pin, I2C
import struct, time

LSM = 0x6A

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
print(f"I2C Devices Scanned: {[hex(i) for i in i2c.scan()]}")

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

def read():
    accel = i2c.readfrom_mem(LSM, 0x28, 6)
    accel = struct.unpack('<hhh',accel)
    return accel

prev = [0,0,0]
down_event = 0
up_event = 0
dot_time = 1000 # in ms
dash_time = 2000 # in ms
diff = 0
led = Pin(0, Pin.OUT)
led.low()
i = 1
dawg = read()
prev = read()
while True:
    dawg = read()
    delta = dawg[i] - prev[i]
    print(f"{i}: {delta}")
    if delta > 400:
        up_event = time.ticks_ms()
        print(f"up! {up_event}")
        diff = up_event - down_event
        print(f"delta time: {diff}")
        led.low()
    if delta < -400:
        print(f"down. {down_event}")
        down_event = time.ticks_ms()
        led.high()
    if diff > dot_time and diff < dash_time:
        print("DOT!")
        up_event = down_event = diff = -1
    if diff > dash_time:
        print("DASH!")
        up_event = down_event = diff = -1
    print(f"status - last down: {down_event}, last up: {up_event}")
    prev = dawg
    time.sleep(0.2)
