import numpy as np
a = np.arange(6)

print('Our array is:')
print(a)

print('Applying id() function:')
print(id(a))

print('a is assigned to b:')
b = a
print(b)
print(id(b))