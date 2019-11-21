import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0, 10,1.5)
print x
y = np.sin(x)
z = np.cos(x)
t = np.tan(x)
print y
a = plt.plot(x,y)
b = plt.plot(x,z)
c = plt.plot(x,t)
print c
#plt.plot(3,1)

plt.show()

