import numpy as np
import matplotlib.pyplot as plt

n = 1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0,1,n)


plt.scatter(X,Y,edgecolors='white')
plt.scatter(Y,X,edgecolors='red')
plt.show()