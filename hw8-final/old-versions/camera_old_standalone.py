import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# Holy mother of good gracious this needs a rewrite. Only had 48 hrs so not worried ATM, if it works then it works.
global count_inline

def find_arm_center(image_to_analyze, lower, upper):
    x, y, w, h = [0, 0, 0, 0]  # for initialization

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image_to_analyze, lower, upper)
    output = cv2.bitwise_and(image_to_analyze, image_to_analyze, mask=mask)

    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        boundingRect = cv2.boundingRect(c)
        x, y, w, h = boundingRect

        # find center of largest contour, c.
        M = cv2.moments(c)
        if M["m00"] > 20:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # If a relevant color contour is found, and is large enough.
            return [cx, cy]
        else:
            # If a relevant color contour is found, but is not large enough.
            return True
    else:
        # If no relevant contour is found.
        return False
    # This shouldn't ever occur...
    return None

def display_magnet_center(magnet_center):
    if type(magnet_center) is list:
        mx, my = magnet_center
        cv2.circle(frame, (mx, my), 2, (0, 0, 255), 2)
        cv2.putText(frame, "<Magnet Center>", (mx + 10, my - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 255), 2)
        cv2.putText(frame, f"Arm Center Coordinates: ({mx}, {my})", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1)
    elif type(magnet_center) is True:
        cv2.putText(frame, f"Arm Center Coordinates: Detected, need larger mass", (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1)
    else:
        cv2.putText(frame, f"Arm Center Coordinates: N/A", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def display_relative(magnet_center, cx):
    if type(magnet_center) is list and cx is not None:
        mx, my = magnet_center
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

def mqtt_publish(msg):
    client.publish(mqtt_thread, msg)
    print(f"message sent to mqtt:, {msg}!")

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
        mqtt_publish("grab")
        count_inline = 6
        print("grab")
        # grab_status = True # Leave uncommented for final test!


def display_valid(valid):
    if valid:
        cv2.putText(frame, f"Sending!", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 1)
    else:
        cv2.putText(frame, f"Not Sending!", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 1)

def find_largest_color_contour(original_image, image_to_analyze, lower, upper, magnet_center, valid_to_send):
    x, y, w, h = [0, 0, 0, 0] # for initialization

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image_to_analyze, lower, upper)
    output = cv2.bitwise_and(image_to_analyze, image_to_analyze, mask=mask)

    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, (0, 0, 255), 3)

        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        # x, y, w, h = [0, 0, 0, 0]
        boundingRect = cv2.boundingRect(c)
        x, y, w, h = boundingRect
        # print(f"x,y,w,h: {boundingRect}")

        # draw the biggest contour (c) in Blue
        cv2.drawContours(original_image, [c], -1, (255, 255, 0), 2)
        # draw it as a box
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # find center of largest contour, c.
        M = cv2.moments(c)

        area_of_object = 5
        if M["m00"] > 5:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # print(f"c: {c}, type: {type(c)}")

            display_magnet_center(magnet_center)
            display_relative(magnet_center, cx)
            display_valid(valid_to_send)

            if type(magnet_center) is list:
                status = display_relative(magnet_center, cx)
                corrective_action(status, valid_to_send)

            # draw it as a point/circle
            cv2.circle(frame, (cx, cy), 2, (255, 0, 255), -1)
            cv2.putText(frame, "DA SPARE RIB", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Center Coordinates: ({cx}, {cy})", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            # Display Everything as a Window
            cv2.imshow('greentrack', (np.hstack([output, original_image]))) # dummy. you return so it won't show if you don't include this.
            return [cx, cy]
        else:
            display_magnet_center(magnet_center)
            display_relative(magnet_center, None)
            display_valid(valid_to_send)
            # If a contour of the right type is detected, but needs a larger area.
            cv2.putText(frame, "Piece Center Coordinates: Detected, need larger mass", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            # Display Everything as a Window
            cv2.imshow('greentrack', (np.hstack([output, original_image])))
            return True
    else:
        display_magnet_center(magnet_center)
        display_relative(magnet_center, None)
        display_valid(valid_to_send)
        cv2.putText(frame, "Piece Center Coordinates: N/A", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        # Display Everything as a Window
        cv2.imshow('greentrack', (np.hstack([output, original_image])))
        return False
    return None

def grab_ms():
    return int(time.time() * 1000) % 1000

def grab_second():
    return int(int(time.time() * 1000) % 10000 / 1000)

# define a video capture object
vid = cv2.VideoCapture(0) # Default Webcam
# vid = cv2.VideoCapture(1) # If using DroidCam (external phone camera)

# mqtt stuff!
mqtt_thread = "arm"
broker_address = "10.243.73.88"
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

# "Main" loop
while(True):
    current_t = int(grab_ms())
    # mod here divides how many times it does this (realy jank)
    # print(f"current t:{current_t}, last t: {last_t}, valid:{valid}")
    if valid is True:
        valid = False
    # currently set to every half second
    if (current_t > 220 and current_t < 250):
        # print(f"New time! tenth of a second:{current_t}, second:{grab_second()}")
        valid = True
        last_t = current_t
        print(f"count_inline:{count_inline}")
    else:
        # print("Same time.")
        valid = False
    # print(f"sec:{grab_second()}, ms:{current_t}, valid:{valid}")

    ret, frame = vid.read()
    cv2_image = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

    # lower_g = [10, 60, 15] # Green is pretty lighting dependent...
    # upper_g = [80, 210, 80]
    # lower_g = [10, 50, 0] # For more bright lighting
    # upper_g = [90, 255, 90]
    # lower_g = [60, 100, 30] # For more bright lighting
    # upper_g = [125, 200, 60]
    lower_g = [100, 150, 80]  # For webcam tests
    upper_g = [120, 190, 120]
    magnet_center = find_arm_center(cv2_image, lower_g, upper_g)
    # print(f"magnet center type: {type(magnet_center)}, data: {magnet_center}")

    lower_b = [0, 30, 90]
    upper_b = [70, 140, 255]
    obj_center = find_largest_color_contour(frame, cv2_image, lower_g, upper_g, magnet_center, valid)
    # print(f"Blue Object Center: {obj_center}")
    # print(f"time: {time.time()}, curr sec {grab_second()}, current ms: {grab_ms()}, current_t: {current_t}, last_t: {last_t}")
    #
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
