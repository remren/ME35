# for shell input: https://forums.raspberrypi.com/viewtopic.php?t=347661
# shell input ): it's 5:05 am why am i like this: https://forum.micropython.org/viewtopic.php?t=7325

import uasyncio as asyncio
from machine import Pin, UART
import time, sys, uselect

uart = UART(1, 115200, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

async def read():
    while True:
#         try:
#             print("read attempt!")
        s = uart.readline()
        print("test")
        if s:
            s = s.decode()
            print(f" >> {s}")
#         except:
#             print("nothing to read")
        await asyncio.sleep_ms(10)
            
async def sendshell():
    shell = None
    prev = None
    initial = True
    msg_to_send = ""
    spoll=uselect.poll()
    spoll.register(sys.stdin,uselect.POLLIN)
    while True:
        time_info = time.localtime()
#         try:
#         print("before stdin")
#         for i in range(3):
#             print(f"before i:{i}")
#             shell = sys.stdin.read(1)
#             print(f"after i:{i}")
#             await asyncio.sleep_ms(1)
#         asyncio.wait_for_ms(sys.stdin.read(1), 1)
        if spoll.poll(0):
            shell = (sys.stdin.read(1))
#         print("after stdin")
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
#         except:
#             print("error in shell")
        await asyncio.sleep_ms(10)
        
async def main(duration):
    loop = asyncio.new_event_loop()
    loop.create_task(read())
    loop.create_task(sendshell())
    await asyncio.sleep(duration)
#     loop.run_forever()
    
def code(): 
    try:
        asyncio.run(main(99)) # runs everything for __ amount of time
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('you are done, clear state')
        
code()
