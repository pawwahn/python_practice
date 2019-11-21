import numpy as np
a = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
b = [[1], [2], [3]]
np_a = np.asarray(a)
#print(np_a)
np_b = np.asarray(b)
#print(np_b)

c = np_a * np_b
print(c)
