import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import tracking

def display_relative(magnet_center, cx):
    if type(magnet_center) is list and cx is not None:
        mx = magnet_center[0]
        my = magnet_center[1]
        lock_region = 20  # In pixels, change for range of lock
        if (cx > mx + lock_region):
            cv2.putText(frame, f"Object is: Right of Arm", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1)
            return "right"
        elif (cx < mx - lock_region):
            cv2.putText(frame, f"Object is: Left of Arm", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1)
            return "left"
        else:
            cv2.putText(frame, f"Object is: Inline with Arm!", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (100, 255, 100), 1)
            return "inline"
    else:
        cv2.putText(frame, f"Object is: N/A to Arm ):", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 1)
        return "n/a"

def corrective_action(status, valid_to_send):
    global count_inline, grab_status
    if status == "right" and valid_to_send and grab_status is False:
        mqtt_publish("tail_right")
        if count_inline > 5:
            count_inline -= 1
    if status == "left" and valid_to_send and grab_status is False:
        mqtt_publish("tail_left")
        if count_inline > 5:
            count_inline -= 1
    if status == "inline" and valid_to_send and grab_status is False:
        count_inline += 1
        print(f"inline: {count_inline}")
    if count_inline == 10 and valid_to_send and grab_status is False:
        count_inline = 6
        print("grab")
        # grab_status = True # Leave uncommented for final test!

def mqtt_publish(msg):
    client.publish(mqtt_thread, msg)
    print(f"message sent to mqtt:, {msg}!")
def grab_ms():
    return int(time.time() * 1000) % 1000
def grab_second():
    return int(int(time.time() * 1000) % 10000 / 1000)

# define a video capture object
vid = cv2.VideoCapture(0) # Default Webcam
# vid = cv2.VideoCapture(1) # If using DroidCam (external phone camera)

# mqtt stuff!
mqtt_thread = "arm"
broker_address = "10.243.40.199"
client = mqtt.Client(mqtt_thread)
client.connect(broker_address)
print('Connected to %s MQTT broker' % broker_address)

# To stop program from sending mqtt stuff at an insane rate
valid = False
current_t = 0
last_t = 0

divisions = 0
count_inline = 0
grab_status = False

track = tracking.Tracking()

saved_arm = None
saved_piece = None
saved_divider = None
dividing_line = 0

upper_region_count = 0
lower_region_count = 0

pickup_status = False
pickup_count = 0
finished_status = False

# "Main" loop
while(True):
    current_t = int(grab_ms())
    if valid is True:
        valid = False
    # currently set to every half second
    if (current_t > 220 and current_t < 250):
        valid = True
        last_t = current_t
        # print(f"count_inline:{count_inline}")
    else:
        valid = False

    ret, frame = vid.read()
    cv2_image = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

    # lower_g = [100, 30, 80]  # For webcam tests
    # upper_g = [120, 190, 120]
    # lower_b = [60, 100, 160]  # For webcam tests
    # upper_b = [80, 130, 190]

    lower_g = [45, 80, 0]  # For final
    upper_g = [75, 125, 55]
    lower_b = [5, 65, 150]  # For final
    upper_b = [45, 100, 255]
    lower_o = [200, 100, 0] # For final
    upper_o = [255, 150, 40] # For final

    arm = track.find_contour(cv2_image, lower_g, upper_g)
    piece = track.find_contour(cv2_image, lower_b, upper_b, 1)
    divider = track.find_contour(cv2_image, lower_o, upper_o)

    if type(arm) is list:
        saved_arm = arm

    if type(piece) is list:
        saved_piece = piece

    if type(divider) is list:
        saved_divider = divider
        dividing_line = saved_divider[0]

    track.draw_contour(frame, saved_arm, 50, 255, 50, "arm")
    track.draw_contour(frame, saved_piece, 255, 50, 25, "Piece Center")
    track.draw_contour(frame, saved_divider, 50, 100, 255, "Divider")

    track.display_text_valid(frame, valid)
    track.display_text_arm_center(frame, saved_arm, arm)
    track.display_text_piece_center(frame, saved_piece, piece)

    if type(piece) is list:
        if piece[1] > dividing_line and valid:
            upper_region_count += 1
            lower_region_count //= 2

        if piece[1] < dividing_line and valid:
            lower_region_count += 1
            upper_region_count //= 2

    track.display_dividingline(frame, dividing_line)
    track.display_text_regions(frame, upper_region_count, lower_region_count)

    if lower_region_count > 5 and valid and not pickup_status:
        mqtt_publish("grab_lower")
        pickup_status = True
    if upper_region_count > 5 and valid and not pickup_status:
        mqtt_publish("grab_upper")
        pickup_status = True

    success_y_line = 100
    if pickup_status and saved_piece[1] < success_y_line and valid:
        pickup_count += 1
    if pickup_count > 6 and True:
        track.display_text_success(frame)

    track.display_successline(frame, success_y_line)

    track.display_window(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
