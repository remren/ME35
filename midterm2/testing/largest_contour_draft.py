import numpy as np

cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
# image_to_analyze = np.array(cam.raw_image)
image_to_analyze = cv2_image
b,g,r = cv2.split(cv2_image)
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY)
# cam.show(grey)  # shows any cv2 image in the same spot on the webpage (third image)
# image3 = Image.fromarray(grey)
# textBox.innerText=repr(np.sum(grey))

# red color boundaries [B, G, R]
# lower = [50, 20, 80]
# upper = [100, 100, 255]
# lower_r = [100, 100, 160]
# upper_r = [230, 180, 255]

def find_largest_color_contour(lower, upper, color):
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image_to_analyze, lower, upper)
    output = cv2.bitwise_and(image_to_analyze, image_to_analyze, mask=mask)
    
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, (0,0,255), 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        if color == "red":
            # draw the biggest contour (c) in Red
            cv2.rectangle(output,(x,y),(x+w,y+h),(255,0,0),2)
        else:
            # draw the biggest contour (c) in Green
            cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

    # show the images
    display(Image.fromarray((np.hstack([cam.raw_image, output]))))

    # Return area of the biggest contour
    return w*h

# # Red Testing
# lower_Red = np.array([100, 100, 160])
# upper_Red = np.array([230, 180, 255])
# mask_r = cv2.inRange(cv2_image, lower_Red, upper_Red)
# res_r = cv2.bitwise_and(cv2_image, cv2_image, mask = mask_r)
# display(Image.fromarray(res_r))
# # print(np.shape(res_r))
# # print(np.shape(mask_r))

# # Green Testing
# lower_Green = np.array([0, 100, 80])
# upper_Green = np.array([180, 255, 100])

# mask_g = cv2.inRange(cv2_image, lower_Green, upper_Green)
# res_g = cv2.bitwise_and(cv2_image, cv2_image, mask = mask_g)
# display(Image.fromarray(res_g))
# # print(np.shape(res_g))
# # print(np.shape(mask_g))

# Find Largest Green
lower_g = [20, 80, 20]
upper_g = [140, 255, 90]
area_g = find_largest_color_contour(lower_g, upper_g, "green")
    
# Find Largest Red
lower_r = [20, 20, 120]
upper_r = [110, 100, 255]
area_r = find_largest_color_contour(lower_r, upper_r, "red")

if (area_g == area_r):
    display("[RESULT] Both colors are the same size.")
elif (area_g > area_r):
    display("[RESULT] Green is larger in size.")
else:
    display("[RESULT] Red is larger in size.")
    
import requests

# https://airtable.com/appuCYgDyr8AZA6XH/tblGydkwtSmHpa5pY/viwgCUqz42evVi04I/recMvkcH9nUrHk1KK

### ! DELETE WHEN PUSHING TO GIT ! ###
key = ''

fields = []

# /v0/{baseId}/{tableIdOrName}/{recordId}
url = "https://airtable.com/v0/appuCYgDyr8AZA6XH/tblGydkwtSmHpa5pY/recMvkcH9nUrHk1KK"
headers = {'Authorization':'','Content-Type':'application/json'}
reply = requests.get(url, headers=headers)
if reply.status_code == 200:
    reply = reply.json() # JSON array of info
    fields = [x['fields'] for x in reply]

display(fields)
