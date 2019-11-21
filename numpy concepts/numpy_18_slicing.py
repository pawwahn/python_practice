import numpy as np

a = np.array([1,2,3,4,5,6])
print "array A is ",a
print "slicing a[0] is", a[0]
print "slicing a[0:] is", a[0:]
print "slicing a[:3] is", a[:3]
print "slicing a[:3,] is", a[:3,]
print "slicing a[2:4] is", a[2:4]
print "type of slicing a[2:4] is", a[2:4],"\t",type(a[2:4])
