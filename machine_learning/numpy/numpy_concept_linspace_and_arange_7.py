import numpy as np

#linspace(a,b,c) -- splits the elements from a to b in c parts
a = np.linspace(10,21,5)
print(a)

#logspace - num=2
b = np.logspace(1,2, num=10)
print(b)

#logspace - base=2
c = np.logspace(1,2, base=2)
print(c)