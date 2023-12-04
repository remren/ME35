import cv2
import numpy as np


# define a video capture object
vid = cv2.VideoCapture(0)

def find_largest_color_contour(original_image, image_to_analyze, lower, upper, color):
    x, y, w, h = [0, 0, 0, 0]

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

        # show the images
        if color == "red":
            # draw the biggest contour (c) in Red
            cv2.rectangle(output, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('dummy', (np.hstack([output, image_to_analyze])))

        else:
            # draw the biggest contour (c) in Green
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('greentrack', (np.hstack([output, original_image])))


    # Return area of the biggest contour
    # return w * h
    if x is not None or y is not None:
        return [x, y]

while(True):
    ret, frame = vid.read()
    cv2_image = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Find Largest Green
    # lower_g = [20, 80, 20]
    # upper_g = [140, 255, 90]
    lower_g = [90, 100, 90] # NOLOP
    upper_g = [110, 255, 130]
    # Find Largest Red
    lower_r = [20, 20, 120]
    upper_r = [110, 100, 255]
    position = find_largest_color_contour(frame, cv2_image, lower_g, upper_g, "green")

    if position :
        print()
    # print(position)

vid.release()
cv2.destroyAllWindows()