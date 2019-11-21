import numpy as np

# 3 types of indexing methods in numpy. they are: field access, basic slicing and advanced indexing

a = np.arange(5)
print(a)
s = slice(2, 5, 2)
print(a[s])

print("****>")
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12, 13]])
print("b[0,...] : {} ".format(b[0, ...]))
print("----->")
print("b[1,...] is : {}".format((b[1, ...])))
print("----->")
print("b[...,1] is : {}".format(b[..., 1]))
print("----->")
print("b[...,2:] is : {}".format(b[..., 2:]))
print("----->")
print("b[...,3] is : {}".format(b[..., 3]))