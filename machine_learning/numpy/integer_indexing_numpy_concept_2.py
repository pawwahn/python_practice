import numpy as np

a = np.array([[1,  2, 3], [4,  5,  6], [7,  8,  9], [10, 11, 12]])
print(a)
rows = np.array([[0, 0], [3, 3]])
cols = np.array([[0, 2], [0, 2]])
y = a[rows, cols]
print("yyyyyyy")
print(y)
print("/----------------------/")
a = np.array([[1,  2, 3, 4], [4,  5,  6, 7], [8,  4,  0, 9], [7, 4, 9, 6]])
print("aaaaaaaaaaaaaaaaaa")
print(a)
r = np.array([[0, 2, 3],[1, 3, 2]])
c = np.array([[1, 2, 3], [3, 1, 2]])
print("***>>")
z = a[r, c]
print(z)

