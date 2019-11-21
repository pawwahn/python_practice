import numpy as np
a = np.array([1.0,5.55, 126, 0.567, 25.132])
print(a)

b = np.around(a, decimals=1)
c = np.around(a, decimals=-1)
print("-->>")
print(b)
print("----")
print(c)