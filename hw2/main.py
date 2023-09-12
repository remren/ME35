from machine import Pin, UART
import time

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

RXE = True
blocking_delay = 0.1

print(uart)

bad_handshake = True

a = 0
while bad_handshake:
    uart.write('1')
    hs = uart.any()
    print(hs)
    if hs is not 0:
        bad_handshake = False
        print("successful handshake!")
    a += 1
    print(a)
    time.sleep(0.1)


print("beginning fred")
uart.write('fred\n')        # write the 4 characters
fred = uart.read()         # read characters, returns bytes
print(fred)
# uart.write('rocks\n')
# fred += uart.readline()     # read until a \n character is sent
# string_fred = fred.decode() # goes from bytes to a string
# print(fred)
# print(string_fred)
