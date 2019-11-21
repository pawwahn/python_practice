import numpy as np

a = np.arange(0, 20, 2)

print("Numpy a is: {} \n ".format(a))
b = a.reshape(2, 5)
print("Reshape of a to b(2,5) is : \n {} \n".format(b))


c = b.copy()
print("copy of b to c and new c is : \n {} \n ".format(c))

print("Transpose of c is : \n {} \n".format(c.T))
print("Reshape of c--> : \n {} \n".format(c.reshape(5, 2)))
print("numpy array c is: \n {} \n ".format(c))
