import numpy as np

a = np.arange(9).reshape(3,3)
print(a)

y = np.where(a>3)
print(y)

print(a[y])

condition = np.mod(a,2) == 0
print(condition)

print('Extract elements using condition')
print(np.extract(condition, a))