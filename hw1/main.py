from machine import Pin
import time

led = Pin(0, Pin.OUT)
constant = Pin(1, Pin.OUT)

dot_delay = 0.1

name = ".-. . -- -.--" # Remy



def dot():
    led.high()
    time.sleep(dot_delay)
    led.low()

def dash():
    led.high()
    time.sleep(4 * dot_delay)
    led.low()
    
def slash():
    dash()
    dot()
    dot()
    dash()
    dot()

def main():
    constant.low()
    for morse in name:
        if morse == ".":
            dot()
            print(".")
        if morse == "-":
            dash()
            print("-")
        if morse == "/":
            slash()
            print("/")
        time.sleep(0.2)
    time.sleep(2)
    # Keep high after initial message is sent.
    led.high()
    constant.high()
    
main()
    

