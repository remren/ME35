from machine import Pin, PWM
import time

pin=PWM(Pin(15))

btn_slower=Pin(27, Pin.IN, Pin.PULL_DOWN)
btn_faster=Pin(26, Pin.IN, Pin.PULL_DOWN)

duty = 0

pin.freq(50) #set the frequency of the pulses
pin.duty_ns(duty)

while True:
    print(f'fast? {btn_faster.value()}')
    print(f'slow? {btn_slower.value()}')
    time.sleep(0.1)

# while True:
#     print(btn_faster.value())
#     print(btn_slower.value())
#     if btn_faster.value() == 1:
#         duty += 10000
#         pin.duty_ns(duty)
#     if btn_slower.value() == 1:
#         duty -= 10000
#         pin.duty_ns(duty)
#     time.sleep(.01)
#     print(duty)

