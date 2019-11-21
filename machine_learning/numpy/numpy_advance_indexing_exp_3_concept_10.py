import numpy as np
x = np.array([[0,  1,  2], [3,  4,  5], [6,  7,  8], [9, 10, 11]])
print('Our array is:')
print(x)
print('\n')

print("1st way of integer indexing is as below:")
y = x[1:4, 1:3]
print(y)
print("\n")

print("2nd way of integer indexing is as below:")
z = x[1:4,[1,2]]
print(z)


