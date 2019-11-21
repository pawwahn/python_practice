import numpy as np

a = np.arange(0,22,3)

b = a.reshape(2, 4)
print(b)

c = a.reshape(2, 4)
print(c)

for x,y in np.nditer([c, b]):
    print("---")
    print("{}:{}".format(x,y))