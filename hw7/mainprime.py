# This is the code for the "solo" Pico.
# It will handle the motors and servos.
# It will communicate with the "antenna" Pico (PC <-> Pico) via
#	bluetooth, in a sequential manner.

"""
    PLAN:
        # 1. Constantly look for connection. If no connection, keep searching.
        #		1a. Only move on if connection is successful.
        #		1b. Skip the check if there is an active connection.
        #		1c. (Extra) If time, add an auto-reconnect from idle.
        # 2. Read in data from the "antenna" Pico over Bluetooth. Blocking?
        # 3. Based on that data, change the state of the motors/servos.
        # 4. Send data to the "antenna" Pico over Bluetooth, reporting
        #	 the current state of the motors/servos.
    
"""

import ble_wrapper, ble
import time
import movement

def main():
    loop = 0 # DEBUG
    bluetooth  = ble_wrapper.BLEWrapper(False, 15)
    bluetooth_success = False
        
    while True:
        # 1. Constantly look for connection. If no connection, keep searching.
        #		1a. Only move on if connection is successful.
        #		1b. Skip the check if there is an active connection.
        #		1c. (Extra) If time, add an auto-reconnect from idle.
        bluetooth_success = bluetooth.ble_status()
#         print(f"bt_success:{bluetooth_success}") # DEBUG
        if not bluetooth_success:
            bluetooth_success = bluetooth.ble_connect() # ble_connects returns a boolean
            print(f"Successful connection: {bluetooth_success}") # DEBUG
        time.sleep(0.1)
        
        # 2. Read in data from the "antenna" Pico over Bluetooth.
        received_data = bluetooth.ble_read()
#         print(f"received_data:{received_data}, loop:{loop}") # DEBUG
        bluetooth.ble_idle_disconnect(received_data) # Disconnect from idle to allow for reconnect in 1c.
        # 3. Based on that data, change the state of the motors/servos.
        print(f"received_data: {received_data}")
        if received_data is not None:
            movement.move(received_data) # from movement! will change motor states.
            time.sleep(4)
       
        time.sleep(4)
        loop += 1
main()