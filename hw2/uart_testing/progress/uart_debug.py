import uasyncio as asyncio
from machine import Pin, UART
import time, sys

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

async def read():
    while True:
        await asyncio.sleep_ms(10)
        try:
            print("read attempt!")
            s = uart.readline()
            if s:
                print(f" >> {s}")
        except:
            print("nothing to read")
        
async def write(msg):
    while True:
        await asyncio.sleep_ms(10)
        try:
            print("write attempt.")
            uart.write(msg)
        except:
            print("could not write")
            
async def sendshell():
    initial = True
    while True:
        await asyncio.sleep_ms(1)
        try:
            print("shell attempt")
            shell = sys.stdin.read(1)
            if shell and initial:
                print(f" << {shell}", end="")
                initial = False
            elif shell:
                print(shell, end="")
            if shell is None:
                initial = True
                
        except:
            print("error in shell")
        
async def main(duration):
    print("loop!")
    loop = asyncio.new_event_loop()
    print("run read")
    loop.create_task(read())
    print("post read")
    loop.create_task(write("hey!"))
    loop.create_task(sendshell())
    await asyncio.sleep(duration)
#     loop.run_forever()
    
def code(): 
    try:
        asyncio.run(main(20)) #start everything running for 10 sec
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('you are done, clear state')
        
code()