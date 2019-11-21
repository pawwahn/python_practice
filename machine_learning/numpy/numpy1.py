import numpy as np

a = np.array([1,2,3])
print("The numpy array a is {}".format(a))
print("The length of numpy array a is {}".format(len(a)))
a[0]=10
print("The numpy array a is {}".format(a))
print(np.ndim(a))

b = np.array(([1,2,3],[4,5,6]))
print(b)

