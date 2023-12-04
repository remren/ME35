# This is code for the "antenna" Pico.
# It will communicate both PC <-> Pico and Pico <-> Pico.
#	- PC <-> Pico is done over Serial.
#	- Pico <-> Pico is done over Bluetooth.
# All code will be done in a sequential manner.

"""
    PLAN:
        # 1. Check for data sent over stdin, data from the UI on the PC.
        # 2. Based on data from stdin, connect or disconnect over Bluetooth.
        #		2a. As this is PC <-> Pico, this is the blocking step.
        #		2b. This means, don't move past this step without a successful connection.
        # 3. Once Bluetooth connection is established, read controller data.
        # 		3a. Process controller data (Doug's code?).
        # 4. Send processed controller data over Bluetooth to the "solo" Pico.
        # 5. Receive data about status of motors/servos from "solo" Pico.

"""

import time, sys, uselect
import ble_wrapper, ble

from machine import Pin


# A non-blocking check for data from the PC over stdin, using spoll.
def frompc_stdin():
#     led_incoming_from_pc = Pin(1, Pin.OUT)
    spoll = uselect.poll()  # Assuming spoll = Select Poll
    spoll.register(sys.stdin, uselect.POLLIN)
    data = ""

    # Use of uselect.poll() to make sys.stdin non-blocking!
    # Awesome! https://forum.micropython.org/viewtopic.php?t=7325
    # Need to read further documentation. Polls the stdin stream.
    # Unsure if in this instance poll() goes to timeout as it =0.
    if spoll.poll(0):
        data = sys.stdin.readline()
    return data


def main():
    loop = 0  # DEBUG
    datafrompc = None
    bluetooth = ble_wrapper.BLEWrapper(True, 50)
    bluetooth_success = False
    prev_datafrompc = None
    
    try:
        while True:
            # 1. Check for data sent over stdin, data from the UI on the PC.
            buffer = str(frompc_stdin())
            if len(buffer):
                datafrompc = buffer.strip()
            #                 print(f"datafrompc:{datafrompc.strip()}, loop:{loop}") # DEBUG

            # 2. Based on data from stdin, connect or disconnect over Bluetooth.
            #		2a. As this is PC <-> Pico, this is the blocking step.
            #		2b. This means, don't send/read over Bluetooth without a successful connection.
            bluetooth_success = bluetooth.ble_status()
            if (datafrompc == "join") and bluetooth_success is False:
                bluetooth_success = bluetooth.ble_connect()
            elif (datafrompc == "quit") and bluetooth_success is True:
                bluetooth.ble_disconnect()
                
#             move_data = None
#             if datafrompc == "l" or datafrompc == "r" or datafrompc == "f" or datafrompc == "b" or datafrompc == "s":
            move_data = datafrompc
#             move_data = None
        
#             datafrompc = "l,l,l,l,r,r,f,f,f,"
#             print(f"datafrompc:{datafrompc}")
#             if datafrompc is not None:
#                 if datafrompc != "join":
#                     parse = datafrompc.split(",")
#     #             print(parse) # DEBUG
#                     mostcommon = max(parse, key=parse.count)
#     #             print(mostcommon)
# 
#                     move_data = mostcommon


            # 4. Send processed controller data over Bluetooth to the "solo" Pico.
            if move_data is not None and bluetooth_success:
                bluetooth.ble_send(move_data)
                print(f"Sent: {move_data}")
                move_data = None

#             # 5. Receive data about status of motors/servos from "solo" Pico.
#             received_data = bluetooth.ble_read()
# 
#             # 6. Send data from "solo" Pico to PC via print() statement.
#             if received_data is not None:
#                 print(f"$$${received_data}")  # $$$ Will be parsed in the UI.

            time.sleep(2)
            loop += 1
            prev_datafrompc = datafrompc
    except KeyboardInterrupt:
        print("KeyboardInterupt!")
    finally:
        print("All set. Ready for new slate.")


main()

