# Overarching UART control code: triggers different subcodes to run depending on
# what user inputs (via number of button clicks)

# Note: there's a .2 second delay after you press the button each time to make
# sure that one longer press of the button doesn't count as multiple clicks

from machine import Pin
import time

import uartmsgs

push_button = Pin(16, Pin.IN)  # 13 number pin is input
uart_client = uartmsgs.UARTMsgs(1, "Bob Ross", "There are no mistakes. Only happy little accidents.")

clicks = 0

def count_clicks(): # counting number of times person presses button
    global clicks
    #print("push ubtton val: ", push_button.value())
    if push_button.value() == 1:
        print("clicked")
        clicks += 1
    #print(clicks)

def send_message(num_clicks):
    if num_clicks == 1:
        print("start LED")
       # send uart message saying to start LED/light sensor code on both picos
    elif num_clicks == 2:
        print("start gamepad")
        # send uart message to start gamepad code on both picos
    elif num_clicks == 3:
        print("start accel")
        # send uart message to start accel code on both picos

while True: # checking how many times buttons was pressed
    button_pressed = push_button.value()
    if button_pressed == 1: # if button is pressed once, start listening for more clicks within 5 seconds
        print("starting to count")
        print(clicks)
        time.sleep(0.3) # makes sure starting button press doesn't get added to click counter
        start = time.time()
        while time.time() < start + 5: # start 5 second timer:
             # start click counter
             count_clicks()
             time.sleep(0.2) # to prevent accidental sequential clicks
        print("timer finished")
        print("clicks: ", clicks)
        send_message(clicks)    
    time.sleep(0.1)