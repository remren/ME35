import cv2

# define a video capture object
vid = cv2.VideoCapture(0)

ret, frame = vid.read()