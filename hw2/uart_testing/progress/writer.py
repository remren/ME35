import uasyncio as asyncio
from machine import Pin, UART
import time

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

i = 0
while True:
    uart.write("hello!")
    print(f"write:{i}")
    i+=1
    print(uart.read())
    time.sleep(0.5)