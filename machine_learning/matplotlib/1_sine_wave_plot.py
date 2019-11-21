import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0,30,0.2)
print(3*np.pi)
print(x)
y = np.sin(x)

plt.title("Sine Wave Graph")
plt.plot(x,y)
plt.show()