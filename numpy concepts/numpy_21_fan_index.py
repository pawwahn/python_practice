import numpy as np

a = np.arange(6).reshape(2,3)
print a

print a[0,1]                            #   1
print a[0,2]                            #   2
print a[1,1]                            #   4
print a[1,:] ,"\n"                             #    [[3 4 5]]
print a[:,2]                             #    [2 5]
print a[:,2].reshape(1,2),"\n"


k = a[abs(a-3) < 2]
print k

print abs(-3)