# for shell input: https://forums.raspberrypi.com/viewtopic.php?t=347661
# shell input ): it's 5:05 am why am i like this: https://forum.micropython.org/viewtopic.php?t=7325

import uasyncio as asyncio
from machine import Pin, UART
import time, sys, uselect

uart = UART(1, 115200, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

async def read():
    while True:
        s = uart.readline()
        if s:
            s = s.decode()
            print(f" >> {s}")
        await asyncio.sleep_ms(10)
            
async def sendshell():
    shell = None
    prev = None
    initial = True
    msg_to_send = ""
    # Use of uselect.poll() to make sys.stdin non-blocking!
    # Awesome! https://forum.micropython.org/viewtopic.php?t=7325
    spoll=uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    while True:
        time_info = time.localtime()
        if spoll.poll(0):
            shell = (sys.stdin.read(1))
        if initial and shell and shell != '\n':
            for i in range(3, 6):
                if time_info[i] < 10:
                    msg_to_send += str(0)
                msg_to_send += str(time_info[i])
                if i == 5:
                    msg_to_send += ' '
                else:
                    msg_to_send += ':'
            msg_to_send += shell
            prev = shell
            initial = False
        elif shell and shell != '\n':
            msg_to_send += shell
        if shell == '\n' and prev is not None and initial is False:
            initial = True
            print(f" You - {msg_to_send}")
            uart.write(msg_to_send)
            msg_to_send = ""
        await asyncio.sleep_ms(10)
        
async def main(duration):
    loop = asyncio.new_event_loop()
    loop.create_task(read())
    loop.create_task(sendshell())
    await asyncio.sleep(duration)
    
def code(): 
    try:
        asyncio.run(main(999)) # runs everything for __ amount of time
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('you are done, clear state')
        
code()
