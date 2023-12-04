import matplotlib.pyplot as plt
import math
import tinyik
import numpy as np
import time
import mqtt
import network

xorigin = 1.0   # circle's x origin
yorigin = 0.0   # circle's y origin
d = 1.0   # circle's diameter
res = 100 # num. of points to describe circle

def find_coords(xo, yo, d, res):
    r = d/2.0	# get radius
    coordinates = []
    delta = 2 * math.pi / res # change in angle between each point
    
    # generate coord for resolution/num of points on circle
    for i in range(res):
        angle = i * delta
        x = xorigin + r * math.cos(angle)
        y = yorigin + r * math.sin(angle)
        coordinates.append((x, y))
    return coordinates

coords = find_coords(xorigin, yorigin, d, res)

xlist, ylist = zip(*coords) # seperates to individual x and y lists for plotting

# Plotting
plt.scatter(xlist, ylist, marker='o', label='Points')

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Giottos Circle')
plt.legend()

# Show the plot
plt.grid()
plt.show()

arm2dof = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])

circle = []
for i in range(res):
    arm2dof.ee = [xlist[i], ylist[i], 0.]
    rounding = np.round(np.rad2deg(arm.angles))
    floatlist = [float(x) for x in rounding]
    circle.append(floatlist)

# to save the coordinates
print(circle)
np.savetxt("circle.txt", circle)

# networking stuff
ssid = 'tufts_eecs'
pwd = 'foundedin1883'
ip = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, pwd)
while not station.isconnected():
    time.sleep(1)
print('Connection successful')
print(station.ifconfig())

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))

pub = mqtt.MQTTClient('test', ip)
pub.connect()
pub.set_callback(whenCalled)

# publish all coord in circle.
for i in range(len(circle)):
    msg = str(circle[i])
    fred.publish('ME035',msg)
    time.sleep(0.1)

fred.disconnect()