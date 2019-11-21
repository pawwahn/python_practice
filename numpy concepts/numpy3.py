#use of numpy over list

import numpy as np
import sys
import time
#import new

size = 2000
l1 = range(size)
l2 = range(size)

a1 = np.arange(size)
a2 = np.arange(size)

start = time.time()

res = [(x+y) for x,y in zip(l1,l2)]

print ("time taken ", (time.time() - start) * 1000)

print (res)

start = time.time()

new_res = a1 + a2

print ("time taken ", (time.time() - start) * 1000)
print (new_res)