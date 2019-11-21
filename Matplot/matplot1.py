import numpy as np
from matplotlib import pyplot as plt
x = np.arange(0,8,0.1)
print(x)
y = np.sin(x)
print(y)
plt.plot(x,y)
plt.show()