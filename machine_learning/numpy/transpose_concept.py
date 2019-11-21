import numpy as np

a = np.arange(0, 15, 2)
print(a)
print("Reshaped matrix is as below:")
b = a.reshape(2, 4)
print(b)

print("Transpose matrix is as below:")
c = b.T
print(c)

print("nditer(c) as follows:")
print(np.nditer(c))
for x in np.nditer(c):
    print(x)

print('\n')

print('Sorted in F-style order:')
c = b.copy(order='F')
print(c)

print('\n')

print('Sorted in C-style order:')
c = b.copy(order='C')
print(c)
print("Transpose of c is as follows:")
print(c.T)


