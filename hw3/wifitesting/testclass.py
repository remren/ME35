import lsm6ds3

test = lsm6ds3.LSM6DS3()
test.init_lsm6ds3()

while True:
    test.readaccel()
