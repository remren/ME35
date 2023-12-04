from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(15))     # the Pico PWM pin
servo.freq(50)
servo.duty_u16(8500)   # sets servo to about down
sleep(2)                           # the 2 secs is to allow the servo to rotate
servo.duty_u16(7500)   # sets servo to about middle
sleep(2)                           # the 2 secs is to allow the servo to rotate
servo.duty_u16(6800)   # sets servo to about high
sleep(2)                           # the 2 secs is to allow the servo to rotate

servo.deinit()                 # stops the PWM signal - 