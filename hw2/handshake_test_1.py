from machine import Pin, UART
import time

uart = UART(1, 9600, timeout = 1000) # set up on UART1 - see pinout - at 9,600 bits per sec
# note that UART0 is often the line connecting your computer and your chip

RXE = True
blocking_delay = 0.1

print(uart)

bad_handshake = True
hs_buffer = ''
attempt = 0

while bad_handshake:
    uart.write('hs123;')
    print('wrote hs123;')
    try:
        hs_buffer = uart.read()
    except:
        print("except")
    print(f'hs_buffer:{hs_buffer}')
    if hs_buffer.decode() is 'hs123;':
        bad_handshake = False
        print("successful handshake!")
    attempt += 1
    print(f'attempt:{attempt}')
#     time.sleep(1)

# print(uart.txdone())
# 
# while uart.txdone():
#     print("data transmission in progress")
#     time.sleep(0.01)

# uart.sendbreak()

print("beginning fred")
uart.write('fred\n')       # write the 4 characters
fred = uart.read()         # read characters, returns bytes
print(fred)
# uart.write('rocks\n')
# fred += uart.readline()     # read until a \n character is sent
# string_fred = fred.decode() # goes from bytes to a string
# print(fred)
# print(string_fred)
