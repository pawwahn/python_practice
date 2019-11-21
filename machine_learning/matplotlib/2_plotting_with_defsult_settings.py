import numpy as np
import matplotlib.pyplot as plt
a = np.arange(-10, 10, 0.1)
#print(a)
c, s = np.cos(a), np.sin(a)
plt.plot(a,s)
plt.plot(a,c)
plt.title("Sine and Cos Waves")
plt.show()
