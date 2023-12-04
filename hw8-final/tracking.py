import cv2
import numpy as np


class Tracking:
    def __init__(self):
        # Magnet/Arm Variables
        self.mx = 0
        self.my = 0

        # Rib Bone/Object Variables
        self.cx = 0
        self.cy = 0

        # Display Variables

    def find_contour(self, image_to_analyze, lower, upper, area=20):
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(image_to_analyze, lower, upper)

        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        if (int(cv2.__version__[0]) > 3):
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)

            # find center of largest contour, c.
            M = cv2.moments(c)
            if M["m00"] > area:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                # If a relevant color contour is found, and is large enough.
                return [cx, cy, c]  # returns center and contour itself
            else:
                # If a relevant color contour is found, but is not large enough.
                print(f"Object with Upper{upper} and Lower{lower} was found but must be larger")
                return True
        else:
            # If no relevant contour is found.
            return False
        # This shouldn't ever occur...
        # return None

    # Params: nparray as image, contour_data=[int, int, numpy.ndarray], int, int, int, str
    def draw_contour(self, image, contour_data, r, g, b, caption):
        # print(f"contour_data type:{type(contour_data)}")
        if type(contour_data) is list:
            x = contour_data[0]
            y = contour_data[1]
            contour = contour_data[2]
            # Contour data itself, as a numpy.ndarray
            cv2.drawContours(image, [contour], -1, (r, g, b), 2)
            # Give contour a caption
            cv2.putText(image, caption, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (r/2, g/2, b/2), 2)
            # Draw dot at center of contour
            cv2.circle(image, (contour_data[0], contour_data[1]), 1, (255, 0, 255), -1)
        # elif type(contour_data) is bool and contour_data is True:
        #     print(f"Object <{caption}> is found, but needs to be larger.")
        # else:
        #     # print(f"Object <{caption}> cannot be found.")

    def display_text_valid(self, image, valid):
        if valid:
            cv2.putText(image, f"Sending!", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
        else:
            cv2.putText(image, f"Not Sending!", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)

    def display_text_arm_center(self, image, contour_data, current_data):
        mx = None
        my = None
        if type(contour_data) is list:
            mx = contour_data[0]
            my = contour_data[1]
        if type(contour_data) is list and type(current_data) is list:
            cv2.putText(image, f"Arm Center Coordinates: ({mx}, {my})", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (100, 255, 100), 1)
        elif type(contour_data) is list and current_data is True:
            cv2.putText(image, f"Arm Center Coordinates: too smol ): Last Known: ({mx}, {my})", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 100), 1)
        else:
            cv2.putText(image, f"Arm Center Coordinates: N/A, Last Known: ({mx}, {my})", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 50, 50),
                        1)

    def display_text_piece_center(self, image, contour_data, current_data):
        mx = None
        my = None
        if type(contour_data) is list:
            mx = contour_data[0]
            my = contour_data[1]
        if type(contour_data) is list and type(current_data) is list:
            cv2.putText(image, f"Piece Center Coordinates: ({mx}, {my})", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (100, 255, 100), 1)
        elif type(contour_data) is list and current_data is True:
            cv2.putText(image, f"Piece Center Coordinates: too smol ): Last Known: ({mx}, {my})", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 100), 1)
        else:
            cv2.putText(image, f"Piece Center Coordinates: N/A, Last Known: ({mx}, {my})", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 50, 50),
                        1)

    def display_successline(self, image, y_line):
        cv2.line(image, (0, y_line), (640, y_line), (204, 255, 255), 1)

    def display_dividingline(self, image, x_line):
        cv2.line(image, (x_line, 0), (x_line, 480), (50, 100, 255), 1)

    def display_text_success(self, image):
        cv2.putText(image, f"SUCCESS!", (320 - 120, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0),
                    3)

    def display_text_regions(self, image, upper_count, lower_count):
        cv2.putText(image, f"Upper Count: {upper_count}, Lower Count: {lower_count}", (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 120),
                    1)

    def display_window(self, image):
        cv2.imshow('Display', image)
