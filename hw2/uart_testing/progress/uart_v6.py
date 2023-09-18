# for shell input: https://forums.raspberrypi.com/viewtopic.php?t=347661
# shell input ): it's 5:05 am why am i like this: https://forum.micropython.org/viewtopic.php?t=7325

import uasyncio as asyncio
from machine import Pin, UART
import time, sys, uselect

uart = UART(1, 115200, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

username = "Frankfurt"
welcome_msg = "i love siracha mayo :D"

async def read():
    while True:
        s = uart.readline()
        if s:
            s = s.decode()
            print(f" >> {s}", end='')
        await asyncio.sleep_ms(10)
            
async def sendstdin():
    # stdin = Standard Input (shell in Thonny)
    shell = None
    msg_to_send = ""
    
    # Use of uselect.poll() to make sys.stdin non-blocking!
    # Awesome! https://forum.micropython.org/viewtopic.php?t=7325
    spoll = uselect.poll()	# Assuming spoll = Select Poll
    spoll.register(sys.stdin, uselect.POLLIN)
    
    while True:
        # localtime() stores in an 8-tuple, H:M:S at indicies 3, 4, 5
        time_info = time.localtime()
        
        # Need to read further documentation. Polls the stdin stream.
        # Unsure if in this instance poll() goes to timeout as it =0.
        if spoll.poll(0):
            shell = sys.stdin.readline()
        
        # Checks if shell is not None or a newline
        if shell and shell != '\n':
            msg_to_send += username + " - "
            
            for i in range(3, 6):
                if time_info[i] < 10:
                    msg_to_send += str(0)
                msg_to_send += str(time_info[i])
                if i == 5:
                    msg_to_send += ' '
                else:
                    msg_to_send += ':'
    
            msg_to_send += shell
            print(f" << {msg_to_send}", end='')
            uart.write(msg_to_send)
            msg_to_send = ""
            shell = None
        await asyncio.sleep_ms(10)
        
async def main(duration):
    print(welcome_msg)
    asyncio.create_task(read())			# read task
    asyncio.create_task(sendstdin())	# send stdin task
    await asyncio.sleep(duration)		# sleeps for duration secs
    
def code(): 
    try:
        asyncio.run(main(999)) # runs everything for __ seconds
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  
        print('All set! There will be a clear state now.')
        
code()
