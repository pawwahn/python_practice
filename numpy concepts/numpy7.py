import numpy as np
a = np.array([[1,2,3],[3,4,5],[5,6,7]])
print a,a.size
print "\n"
b = np.array([(1,2,3),(3,4,5),(4,5,6)])
print b,np.ndim(b),np.size(b),"\n"

c = np.hstack(a)
print c,"\n"
d = np.vstack(a)
print "\n d--\n",d,"\n"

print (a+b)*a,"\n"
print a+(b*a),"\n\n"

j = np.array([[1,2,3,4],[3,4,5,8],[5,6,7,8],[1,2]])
print j.shape,"\n"


j = np.array([[1,2,3,4],[3,4,5,8],[5,6,7,8],[1,2,3,4]])
print j.shape