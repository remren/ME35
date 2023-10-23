import matplotlib.pyplot as plt
import math

# Initial Example
# x = [0,1,2]
# y = [0,1,0]

#FORWARD
# L = [ 1, 1]
# theta = [10, -10]

#INVERSE
x_e, y_e = 1.3, 0.2  #desired end position

# some code to calculate the two angles

        
#your code from above in here

fig, ax = plt.subplots()
ax.plot(x,y)

ax.set(xlabel='X position', ylabel='Y position', title='Arm position')
#ax.grid()
plt.show()