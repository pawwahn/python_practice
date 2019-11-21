import numpy as np

dt = np.dtype([('name', 'S10'),('age', int)])
print(dt)
a = np.array([("raju",21),("anil",25),("ravi", 17), ("amar",27)], dtype = dt)


print('Our array is:')
print(a)
print('\n')

print('Order by name:')
print(np.sort(a, order = 'name'))
print(np.sort(a, order = 'age'))
