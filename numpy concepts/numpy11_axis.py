import numpy as np

a = np.array([(1,2,3),(2,3,4),(4,5,6)])
print a,"\n"

print a.sum(axis=0),"\n"             # [ 7 10 13]

print a.sum(axis=1)             # [ 6  9 15]
#print a.sum(axis=2)            # axis is either 0 or 1