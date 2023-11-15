import cv2

# Read the video
cap = cv2.VideoCapture(0)

# Read the first frame
ret, frame = cap.read()

# Set the ROI (Region of Interest)
x, y, w, h = cv2.selectROI(frame)

# Initialize the tracker
roi = frame[y:y+h, x:x+w]
roi_hist = cv2.calcHist([roi], [0], None, [256], [0,256])
roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate the back projection of the histogram
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,256], 1)

    # Apply the MeanShift algorithm
    ret, track_window = cv2.meanShift(dst, (x,y,w,h), term_crit)

    # Draw the track window on the frame
    x,y,w,h = track_window
    img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    # Display the resulting frame
    cv2.imshow('frame',img2)

    # Exit if the user presses 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()