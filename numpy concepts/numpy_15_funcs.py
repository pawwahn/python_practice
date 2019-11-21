# random numpy

import numpy as np
from random import random
import timeit
import time

#a = np.array([(1,2,3,'a',5),(1,2,3,4,'a'),(4,5,6,7)])
a = np.array([(1,2,3,5),(1,2,3,4),(4,5,6,7)])
print "min -> ",np.min(a)
print "max ->",a.max()
print "max ->",np.max(a)
print "position or index of max value in the array",a.argmax()
print "position or index of min value in the array",a.argmin()
print "mean of the array",np.mean(a)
print "median of the numpy array",np.median(a)




