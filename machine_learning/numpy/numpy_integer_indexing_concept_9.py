import numpy as np

x = np.array([[1, 2], [3, 4], [5, 6]])
y = x[[0,1,2], [1,1,0]]    # x[[a],[b]
# this helps in creating the new array [a] from the values of the array by using the positions [b]
print(y)
print("****")
z = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
z1 = z[[3, 2, 1, 3], [2, 2, 1, 2]]  # 3rd arr 2nd ele, 2nd arr 2nd ele, 1st arr 1st ele, 3rd arr 2nd ele
print(z1)
