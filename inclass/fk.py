import matplotlib.pyplot as plt
import math

# Initial Example
# x = [0,1,2]
# y = [0,1,0]

x = [0,1,2]
y = [0,1,0]

L = [ 1, 1]
theta = [10, -10]

#write some code here to replace the values in x,y with calculated values from L, Theta
# NEED TO WRITE?!

#-------- now plot it
fig, ax = plt.subplots()
ax.plot(x,y)

ax.set(xlabel='X position', ylabel='Y position', title='Arm position')
ax.grid()
plt.show() # in Thonny