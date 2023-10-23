import time

while True:
    time_info = time.localtime()
    msg_to_send = ""
    for i in range(3, 6):
        if time_info[i] < 10:
            msg_to_send += str(0)
        msg_to_send += str(time_info[i])
        if i == 5:
            msg_to_send += ' '
        else:
            msg_to_send += ':'
    print(msg_to_send)
    time.sleep(0.2)
