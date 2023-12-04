#ensure is IP adress of CPU mqtt is running on, and pub names match

#proj - make code on computer that connects to buttons that send directions as messages to mqtt on computer that pico listens to
#import Codes.secrets as codes
import time
# from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Remy added libraries
import mqtt
import connect_pico_to_wifi as wifi
import fourwirestepper_wrapper as stepper_wrapper

left_servo=PWM(12)
left_servo.freq(50)
right_servo=PWM(15)
right_servo.freq(50)
tail_servo = PWM(15)
tail_servo.freq(50)
pulley_servo = PWM(14)
pulley_servo.freq(50)
left_led = Pin(17, Pin.OUT, Pin.PULL_UP)
right_led = Pin(1, Pin.OUT, Pin.PULL_UP)

wifi.connect_wifi()
stepper = stepper_wrapper.Stepper(8, 9, 10, 11)

l = 0
r = 0
tail_pos = 1.5

def start_motion():
#     stepper.move_steps(50)
    print(stepper.current_pos())
    for i in range(2):
        stepper.move_steps(25)
        print(stepper.current_pos())
#         stepper.turn_off_motor()
        time.sleep(0.1)
        stepper.move_steps(-25)
        print(stepper.current_pos())
#         stepper.turn_off_motor()
        time.sleep(0.1)
        
def grab():
    # Pull down
    for i in range(2):
        pulley_servo.duty_ns(1200000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
    time.sleep(2)
    # Pull up
    for i in range(2):
        pulley_servo.duty_ns(1800000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
        
def whenCalled(topic, msg):
    print("Received message on topic:", topic.decode())
    print("Message:", msg.decode())
    #print((topic.decode(), msg.decode()))
    message = msg.decode()
#     message = ''
    global l
    global r
    global tail_pos
    if message == "forward":
        print("forward")
        l = 2
        r = 1.2
    elif message == "tail:":
        l=0
        r=0
        pulley_servo.duty_ns(1800000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
    elif message == "down":
        l=0
        r=0
        pulley_servo.duty_ns(1200000)
        time.sleep(.7)
        pulley_servo.duty_ns(0)
    elif message == "grab":
        grab()
    elif message == "tail_left":
        for i in range(100):
            tail_pos = tail_pos + 0.001
            tail_servo.duty_ns(int(tail_pos*1000000))
            time.sleep(.005)
    elif message == "tail_right":
        for i in range(100):
            tail_pos = tail_pos - 0.001
            tail_servo.duty_ns(int(tail_pos*1000000))
            time.sleep(.005)
        tail_servo.duty_ns(int(0))
    elif message == "tail_start":
        tail_pos = 2.5
        while tail_pos > 1.5:
            tail_pos = tail_pos - 0.005
            mult_pos = int(tail_pos*1000000)
            time.sleep(.01)
            tail_servo.duty_ns(mult_pos)
            print(f'Tail Pos: {tail_pos}, Multiplied: {mult_pos}')
        tail_servo.duty_ns(int(0))
    elif message == "wiggle":
        for i in range(4):
            stepper.move_steps(25)
            time.sleep(1)
            stepper.move_steps(-25)
            time.sleep(1)
    elif "step:" in message:
        print(f"moving {message[5:]} steps")
        stepper.move_steps(int(message[5:]))

    elif message == "toggle":
        left_led.toggle()
        right_led.toggle()
        
    left_servo.duty_ns(int(l*1000000))
    right_servo.duty_ns(int(r*1000000))
    time.sleep(.4)
    left_servo.duty_ns(int(0))
    right_servo.duty_ns(int(0))
    

def main():
    try:
#         juliaremy = MQTTClient('arm', '10.243.26.3', keepalive=600)
        #juliaremy = MQTTClient('Test', '10.243.66.94', port=1883, ssl=True, ssl_params={'certfile': 'your_cert.pem'})
        #print('Connected')
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
    except Exception as e:
        print(e)
    finally:
        juliaremy.disconnect()
        stepper.turn_off_motor()
        print('done')
   
main()
