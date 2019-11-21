import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5*np.pi , 0.1)
#print x
y = np.sin(x)
z = np.cos(x)
t = np.tan(y)
#print y
plt.plot(x,y)
plt.plot(x,z)
plt.plot(x,t)

plt.show()
