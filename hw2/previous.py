from machine import Pin, PWM
from utime import sleep
import _thread

# PIN SETUP

morseLed = Pin(15, Pin.OUT) #LED flashing morse name
morseLed.low()
photo_pin = machine.ADC(28) #analog reading for light sensor
lightLed = PWM(Pin(19)) # LED brightness based on light
lightLed.freq(1000)

TIME_UNIT = .2

# MORSE SETUP

morse_dict = {'A':'.-', 'B':'-...',
'C':'-.-.', 'D':'-..', 'E':'.',
'F':'..-.', 'G':'--.', 'H':'....',
'I':'..', 'J':'.---', 'K':'-.-',
'L':'.-..', 'M':'--', 'N':'-.',
'O':'---', 'P':'.--.', 'Q':'--.-',
'R':'.-.', 'S':'...', 'T':'-',
'U':'..-', 'V':'...-', 'W':'.--',
'X':'-..-', 'Y':'-.--', 'Z':'--..'}

def dot(): #1 time unit + 1 btwn
morseLed.on()
sleep(TIME_UNIT)
morseLed.off()
sleep(TIME_UNIT)

def dash(): #2 time units + 1 btwn
morseLed.on()
sleep(TIME_UNIT*2)
morseLed.off()
sleep(TIME_UNIT)

def pause(): # 2 time units between letters
sleep(TIME_UNIT*2)

# LIGHT SENSOR SETUP

def map(val, loval, hival, tolow, tohigh):
if loval <= val <= hival:
newval = (val - loval)/(hival-loval)*(tohigh-tolow) + tolow
return int(newval)
else:
return 0
#raise(ValueError)

#--------------------------#

def core0_thread(): # photo LED
while True:
val = photo_pin.read_u16()
mapped_val = map(val, 0, 2000, 0, 65025) #mapping light sensor vals to led pwm
mapped_val *= 2 # expanding range
lightLed.duty_u16(mapped_val)
sleep(0.1)

def morse_name(name): #no spaces allowed in name
name = name.upper()
while True:
for i in name: # iterate through morse of each letter
print(i, ": ", morse_dict[i])
for symbol in morse_dict[i]:
if symbol == "-":
dash()
elif symbol == ".":
dot()
pause()

def core1_thread():
morse_name(name)

name = input("What is your name? \n")
second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()