import AccelStepper

# num of wires for stepper motor: 4
# on RoboPico, wires were arranged > Motor 1: GP8 has Red, GP9 has Yellow > Motor 2: GP10 has Green, GP11 has Gray
# 200 total steps, so 200 steps for one whole revolution!

# pin0 and 1 are a pair, pin 2 and 3 are a pair. if working with the Adafruit NEMA 17 motor, see their wiring
# suggestion with their motor shield.
class Stepper:
    def __init__(self, pin0, pin1, pin2, pin3):
        self.stepper = AccelStepper.AccelStepper(4, pin0, pin1, pin2, pin3, True)
        # On boot, the position at that time is considered the 0 position.
        self.stepper.set_current_position(0)
        print('Stepper Wrapper: reset to position')
        self.stepper.set_acceleration(250)
        self.stepper.set_max_speed(500)
        
    def move_steps(self, steps):
#         print("Stepper Wrapper: moving...")
        self.stepper.move(steps)
        while self.stepper.run():
            self.stepper.run()
#         print("Stepper Wrapper: done with move :D")
        
    def current_pos(self):
        return self.stepper.current_position()
    
    def turn_off_motor(self):
        self.stepper.disable_outputs()
        