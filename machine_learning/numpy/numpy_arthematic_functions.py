import numpy as np
a = np.arange(-11, 107, 3)
b = a.reshape(5, 8)
print(b)

print(np.reciprocal(b))

print('Applying power function:')
print(np.power(a, 2))
print('\n')
