import numpy as np
x = np.array([[0,  1,  2],[3,  4,  5],[6,  7,  8],[9, 10, 11], [1, 2, 4]])

print('Our array is:')
print(x)
print('\n')

print('The items greater than 5 are:')
print(x[x > 5])

print('The items less than 2 are:')
print(x[x < 2])

