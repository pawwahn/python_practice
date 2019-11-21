from matplotlib import pyplot as plt
import numpy as np
x = np.arange(1,20,2)
y = np.sqrt(x)




plt.title("Subplot 1")

plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.subplot(311)
plt.plot(x,y,label="demo1")
plt.legend()

x1 = np.arange(5,40,3)
y1 = np.sqrt(x1)


plt.title("Subplot 2")

plt.xlabel('x1-axis')
plt.ylabel('y1-axis')
plt.subplot(312)
plt.plot(x1,y1,label="demo 2")
plt.legend()

x2 = np.array([1,2,3,4,5,6,7,8,9,10,11])
y2 = np.sin(x2)
plt.title("Subplot 3")
plt.xlabel("x3 label")
plt.ylabel("y3 label")
plt.subplot(313)
plt.plot(x2,y2,label="demo 3")
plt.legend()



plt.show()