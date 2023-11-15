import connect_pico_to_wifi as wifi_helper
import time
import urequests as requests
import ujson as json
import thermistor
import pico_mqtt_to_adafruit as mqtt_aio
import display
import joypad

wifi_helper.connect_wifi()

### FIELDS FOR REQUEST TO CONNECT TO AIRTABLE ###

### ! DELETE WHEN PUSHING TO GIT ! ###
airtable_token = ''

fields = []

# BEST TUTORIAL! https://dev.to/matthewvielkind/using-python-and-airtable-3bb7
# /v0/{baseId}/{tableIdOrName}/{recordId}
url = "https://api.airtable.com/v0/appuCYgDyr8AZA6XH/tblGydkwtSmHpa5pY/recMvkcH9nUrHk1KK"
headers = {
           'Authorization':f'Bearer {airtable_token}',
           'Content-Type':'application/json'
          }

### END OF FIELDS FOR REQUEST TO CONNECT TO AIRTABLE ###

# Important Variables for Following Functions
reply = None
sender = mqtt_aio.mqttAIO()
display_instance = display.Display()
color = ""
gamepad = joypad.Joypad(1, 19, 18)
gamepad.digital_setup()

# [ FIXED ] ENOMEM error? https://stackoverflow.com/questions/76606812/outofmemory-in-micropython
def get_airtable_color():
    reply = requests.request("GET", url, headers=headers)
    if reply.status_code == 200:
        data = reply.json() # JSON array of info
        airtable_color = data["fields"]["Color"]
        data = None # For memory reset? Just to be safe...
        print(f"Color from AirTable: {airtable_color}") # DEBUG
    reply.close() # Very important to close opened sockets, or memory is quickly gone!
    reply = None # Just to be safe...
    if airtable_color is not None:
        color = airtable_color
        return airtable_color
    
# [ FIXED ] Memory issues? https://github.com/orgs/micropython/discussions/11559
# FIXED MEMORY ISSUE, HAaD CLASS INITIALIZATION IN THE FUNCTION. MEMORY GOBBLER!!!
def send_temp_to_aio():
#     instance_color = get_airtable_color()
#     color = "green" # DEBUG
    # if color == "green", temp will be in F. else, temp is in C.
    temp = thermistor.getTemp()
    print(f"tempF={temp[0]}, tempC={temp[1]}, color={color}") # debug
    # Sends F, C in this order.
    sender.send_temp(temp[0], temp[1])

def update_display_temp():
    print(f"color in update display={color}")
    temp = thermistor.getTemp()
    # formatting: https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    if color == "green":
        temp_text = f"{"{:12.4f}".format(temp[0])} F     "
    else:
        temp_text = f"{"{:12.4f}".format(temp[1])} C     "
    # Wrapper function for object
    display_instance.displaytext(temp_text, 8, 10)

counter = 0
def gamepad_counter(num):
    buttons = gamepad.get_buttons()
#     print(buttons)
    if buttons[2] is True:
        print("increase")
        num += 1
    if buttons[3] is True:
        print("decrease")
        num -= 1
    return num

rough_timer = 0
counter_prev = counter
while True:
    if counter != counter_prev:
        display_instance.changebg(counter % 7)
        counter_prev = counter
    update_display_temp()
#     time.sleep(3)
    counter = gamepad_counter(counter)
#     print(f"counter={counter}")
    time.sleep(0.01)
    rough_timer += 1
    if rough_timer % 40 == 0:
        send_temp_to_aio()
    elif rough_timer % 20 == 0:
        color = get_airtable_color()