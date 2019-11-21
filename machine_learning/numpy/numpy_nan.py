import numpy as np
a = np.array([np.nan, 1, 2, np.nan, 3, 4, 5])
print(a[~np.isnan(a)])
print("----")
a = np.array([1, 2+6j, 5, 3.5+5j])
print(a[np.iscomplex(a)])

