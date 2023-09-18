from machine import Pin, UART
import time

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

RXE = True
blocking_delay = 0.1

print(uart)

uart.write('fred\n')        # write the 4 characters

while RXE:
    RXE = True
    fred = uart.read(2)         # read 2 characters, returns bytes
    if fred is not None:
        print(fred)
        fred += uart.read()         # read all available characters
        print(fred)
        RXE = False
    time.sleep(blocking_delay)

print("WRITING!")
uart.write('rocks\n')
RXE = True

attempts = 0
while RXE:
    try:
        fred += uart.readline()
        string_fred = fred.decode() # goes from bytes to a string
        print("try")
        print(fred)
        print(string_fred)
        RXE = False
    except:
        print(f"nothing new received, attempt:{attempts}")
        RXE = True # not necessary, just for notekeeping
        attempts += 1
    time.sleep(blocking_delay)
    
print("end")
