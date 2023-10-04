from machine import Pin, PWM
import time

pin=PWM(Pin(12))
pin.freq(50) #set the frequency of the pulses
while True:
    print("right")
    pin.duty_ns(350000)  #set width of pulse to 1.5 ms (right
    time.sleep(.5)
    print("middle")
    pin.duty_ns(1000000)  #set width of pulse to 1 ms (middle)
    time.sleep(.5)
    print("left")
    pin.duty_ns(2500000)  #set width of pulse to 2 ms (left)
    time.sleep(.5)
