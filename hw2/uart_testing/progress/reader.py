import uasyncio as asyncio
from machine import Pin, UART
import time

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

# async def receiver True:
#     data = uart.readline()
#     if data:
#         print(data)
#     else:
#         print("nothing new!")

async def receiver():
    while uart.any() < 10:
        await asyncio.sleep_ms(10)
    c = uart.read(10)
    print(c)
    
async def main(duration):
    print("loop!")
    loop = asyncio.new_event_loop()
    print("run read")
    loop.create_task(receiver())
    print("post read")
#     loop.create_task(write("hey!"))
    await asyncio.sleep(duration)
    loop.run_forever()
    
def code(): 
    try:
        asyncio.run(main(10)) #start everything running for 10 sec
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('you are done, clear state')
        
code()