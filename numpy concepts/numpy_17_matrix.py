import numpy as np

a = np.array([(1,2),(3,4),(4,5),(5,6)])
print a,"\n"
new_a = a.reshape(2,4)
print new_a,"\n"

b = np.array([(1,2,3,4),(4,5,5,6)])
print b,"\n"
c = new_a + b.reshape(2,4)
print c,"\n"