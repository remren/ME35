import AccelStepper

# num of wires for stepper motor: 4
# on RoboPico, wires were arranged > Motor 1: GP8 has Red, GP9 has Yellow > Motor 2: GP10 has Green, GP11 has Gray
# 200 total steps, so 200 steps for one whole revolution!
stepper = AccelStepper.AccelStepper(4, 8, 9, 10, 11, True)

print('reset to position')
stepper.set_current_position(0)
stepper.set_acceleration(1000)
stepper.set_max_speed(100)
stepper.move_to(200)
while stepper.run():
#     print(stepper.current_position())
    stepper.run()
stepper.disable_outputs()
print("done")