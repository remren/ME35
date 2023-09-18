# for shell input: https://forums.raspberrypi.com/viewtopic.php?t=347661

import uasyncio as asyncio
from machine import Pin, UART
import time, sys

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

async def read():
    while True:
        await asyncio.sleep_ms(10)
        try:
#             print("read attempt!")
            s = uart.readline()
            if s:
                print(f" >> {s}")
        except:
            print("nothing to read")
        
async def write(msg):
    while True:
        await asyncio.sleep_ms(10)
        try:
            uart.write(msg)
        except:
            print("could not write")
            
async def sendshell():
    shell = None
    prev = None
    initial = True
    msg_to_send = ""
    
    while True:
        await asyncio.sleep_ms(1)
        try:
#             print(f"top - prev:{prev}, shell:{shell}")
            shell = sys.stdin.read(1)
            if initial and shell and shell != '\n':
                print(f" << {shell}", end="")
#                 print(f"prev:{prev}, shell:{shell}")
                msg_to_send += shell
                prev = shell
                initial = False
            elif shell and shell != '\n':
                print(shell, end="")
                msg_to_send += shell
            if shell == '\n' and prev is not None and initial is False:
#                 print("init")
                initial = True
                print('\n', end="")
#                 print(f"final msg:{msg_to_send}")
                write(msg_to_send)
                uart.write(msg_to_send)
#             else if shell and shell != '\n':
#                 print(shell, end="")
#                 prev = shell
#             elif shell and shell != '\n':
#                 print(shell, end="")
        except:
            print("error in shell")
        
async def main(duration):
    loop = asyncio.new_event_loop()
    loop.create_task(read())
#     loop.create_task(write('hey!'))
    loop.create_task(sendshell())
    await asyncio.sleep(duration)
    loop.run_forever()
    
def code(): 
    try:
        asyncio.run(main(20)) # runs everything for __ amount of time
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('you are done, clear state')
        
code()
