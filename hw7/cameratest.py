import cv2
import numpy as np


# define a video capture object
vid = cv2.VideoCapture(0)


# SHOUTOUTS TO SHIIIIV

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ret, frame = vid.read()
    # cv2_image = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    b,g,r = cv2.split(frame)
    red = cv2.subtract(r,g)
    # Blur red channel
    blurred = cv2.GaussianBlur(red, (5, 5), 0)
    # Threshold blurred image
    thresh = cv2.threshold(blurred, 125, 255, cv2.THRESH_BINARY)[1]
    # Find the contours in the threshold image
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour if possible
    largest_contour = max(cnts, key=cv2.contourArea, default=None)
    print("test")
    if largest_contour is not None:
        print("within")
        # highlight largest contour
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        # Find center of largest contour
        M = cv2.moments(largest_contour)
        # area = cv2.contourArea(largest_contour)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            print(f"cx, cy: {[cx, cy]}")
            # return cx, cy

    cv2.imshow("test", frame)
        # cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), thickness=cv2.FILLED)
        # cv2.circle(frame, (cx, cy), 7, (255, 0, 0), -1)
        # cv2.putText(frame, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


    # info.append([area, cX, cY])
    #
    # areas = [row[0] for row in info]
    # order = np.flip(np.argsort(areas))
    # info[order[0]]
vid.release()
cv2.destroyAllWindows()