import numpy as np

#arange function use in numpy

a = np.arange(21)
print(a)
print("---------")
b = np.arange(21,41)
print(b)

#reshape numpy array b

c = b.reshape(4,5)
print(c)

#find itemsize

d = np.arange(50,71)
print(d)
print("Len",len(d))
print("Size",np.size(d))
print("The item size is :{}".format(d.itemsize))
print(d.flags)
print("**********>>>")
e = np.array([1,2,3],dtype=complex)
print(e.flags)