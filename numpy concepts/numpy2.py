import numpy as np
import time
import sys
from sys import getsizeof

#a = np.array([(1,2,3),(4,5,6)])

s = range(100)
print("--------- 1 ",(getsizeof(s)))
print("--------- 2 ",getsizeof(3))
print("--------- 3 ",len(s))
print("--------- 4 ",(getsizeof(3) * len(s)))
print("--------- 40 ",(getsizeof(s) * len(s)))
print("--------------------------------\n")

n = np.arange(100)
print("--------- 5 ",(getsizeof(n)))
print("--------- 6 ",(getsizeof(8)))
print("--------- 7 ",len(n))
print("--------- 8 ",(getsizeof(3) * len(n)))
print("--------- 80 ",(getsizeof(n) * len(n)))

print("-------------------------------22-\n")
print("--------- 9 ",n.size)
print("--------- 10 ",n.itemsize)
print("--------- 11 ",(n.size * n.itemsize))
