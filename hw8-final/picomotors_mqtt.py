#ensure is IP adress of CPU mqtt is running on, and pub names match

#proj - make code on computer that connects to buttons that send directions as messages to mqtt on computer that pico listens to
#import Codes.secrets as codes
import time
from math import fabs
# from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Remy added libraries
import mqtt
import connect_pico_to_wifi as wifi
import fourwirestepper_wrapper as stepper_wrapper

tail_servo = PWM(15)
tail_servo.freq(50)
pulley_servo = PWM(14)
pulley_servo.freq(50)

wifi.connect_wifi()
stepper = stepper_wrapper.Stepper(8, 9, 10, 11)

tail_position = 6500 # most high tail position
pulley_cw = 1
pulley_ccw = 2


def start_motion():
    print("Start Up Motion! - Set Tail to Neutral")
    tail_servo.duty_u16(tail_position)
    print(f"Stepper position: {stepper.current_pos()}")
    for i in range(2):
        stepper.move_steps(25)
        print(f"Stepper position: {stepper.current_pos()}")
#         stepper.turn_off_motor()
        time.sleep(0.1)
        stepper.move_steps(-25)
        print(f"Stepper position: {stepper.current_pos()}")
#         stepper.turn_off_motor()
        time.sleep(0.1)
        
def move_tailservo(position):
    global tail_position
    diff = 0
    if position == "mid":
        diff = tail_position - 7700
    elif position == "low":
        diff = tail_position - 8500
    elif position == "high":
        diff = tail_position - 6800
    steps = 100
    step_delta = int(diff / steps)
    print(f"diff:{diff}, step_delta:{step_delta}, steps:{steps}")
    for i in range(steps):
        tail_position -= step_delta
        tail_servo.duty_u16(int(tail_position))
        time.sleep(.005)
#             print(f"tail_position:{tail_position}")
    print(f"moved servo to: {position}")
    
def move_tailservo_exact(duty_u16_value):
    global tail_position
    diff = tail_position - duty_u16_value
    steps = 100
    step_delta = int(diff / steps)
    print(f"diff:{diff}, step_delta:{step_delta}, steps:{steps}")
    for i in range(steps):
        tail_position -= step_delta
        tail_servo.duty_u16(int(tail_position))
        time.sleep(.005)
#             print(f"tail_position:{tail_position}")
    print(f"moved servo to:	 {position}")
    
def move_pulley(direction, duration):
    if direction == "up":
        pulley_servo.duty_ns(1200000) # CCW max speed is a 2 ms pulse. 1.75 is between 1.5 (stop?) and 2 ms
    else:
        pulley_servo.duty_ns(1800000) # CW lowest speed is a 1 ms pulse. 1.25 is between 1.5 (stop?) and 1 ms
    
    time.sleep(duration) # THE AMOUNT OF TIME THIS IS FOR IN FLOAT, IS HOW LONG THE PULLEY WILL RUN FOR!
    pulley_servo.duty_ns(0) # Stops the pulley_servo
        
# If piece is in the lower position
def move_to_lower():
    # Move to retrieve
    stepper.move_steps(-49)
    time.sleep(0.1)
    move_tailservo("mid")
    # Grab with pulley
    time.sleep(2)
    move_pulley("down", 1)
    time.sleep(.5)
    move_pulley("down", 1)
    time.sleep(3)
    move_pulley("up", 1)
    time.sleep(.5)
    move_pulley("up", 1)
    # Return to original position
    move_tailservo("high")
    stepper.move_steps(+49)
    return None

# If piece is in the upper position
def move_to_upper():
    # Move to retrieve
    stepper.move_steps(-53)
    time.sleep(0.1)
    move_tailservo("low")
    # Grab with pulley
    time.sleep(2)
    move_pulley("down", 1)
    time.sleep(3)
    move_pulley("up", 1)
    # Return to original position
    move_tailservo("high")
    stepper.move_steps(+53)
    return None
        
def grab():
    # Pull down
    for i in range(2):
        move_pulley("down", 0.6)
        time.sleep(.7)
    time.sleep(2)
    # Pull up
    for i in range(2):
        move_pulley("down", 0.6)
        time.sleep(.7)
        
def whenCalled(topic, msg):
    print("Received message on topic:", topic.decode())
    print("Message:", msg.decode())
    #print((topic.decode(), msg.decode()))
    message = msg.decode()
#     message = ''
    global tail_position
    
    if message == "p_down":
        pulley_servo.duty_ns(1800000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
    elif message == "p_up":
        pulley_servo.duty_ns(1200000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
        
    elif "pulley" in message:
        pulley_data = message.split(":") # Data: pulley, direction (string, either "up" or "down", duration pulley is on for as a float
        print(f"pulley_data: {pulley_data}")
        direction = pulley_data[1]
        duration = float(pulley_data[2])
        move_pulley(direction, duration)
        
#         if pulley_data[1] == "up":
#             pulley_servo.duty_ns(1200000) # CCW max speed is a 2 ms pulse. 1.75 is between 1.5 (stop?) and 2 ms
#         else:
#             pulley_servo.duty_ns(1800000) # CW lowest speed is a 1 ms pulse. 1.25 is between 1.5 (stop?) and 1 ms
#         time.sleep(float(pulley_data[2])) # THE AMOUNT OF TIME THIS IS FOR IN FLOAT, IS HOW LONG THE PULLEY WILL RUN FOR!
#         pulley_servo.duty_ns(0) # Stops the pulley_servo
        
    elif "servo" in message:
        servo_data = message.split(":")
        move_tailservo(servo_data[1])
        
    elif message == "grab":
        grab()
        
    elif "step:" in message:
        print(f"moving {message[5:]} steps")
        stepper.move_steps(int(message[5:]))
        
    elif message == "wiggle":
        for i in range(4):
            stepper.move_steps(25)
            time.sleep(0.1)
            stepper.move_steps(-25)
            time.sleep(0.1)
            
    elif message == "grab_upper":
        move_to_upper()
        
    elif message == "grab_lower":
        move_to_lower()
    
def main():
    try:
        juliaremy = mqtt.MQTTClient('device', '10.243.40.199', keepalive=600)
        juliaremy.connect()
        print('Connected')
        juliaremy.set_callback(whenCalled)
    except OSError as e:
        print(e)
        print('Failed')
        return
    juliaremy.subscribe('arm')
    
    #publishing - not needed
    try:
        start_motion()
        while True:
            juliaremy.check_msg()
            #print#check subscriptions - you might want to do this more often
            time.sleep(.01)
#     except Exception as e:
#         print(e)
    finally:
        juliaremy.disconnect()
        stepper.turn_off_motor()
        print('done')
   
main()