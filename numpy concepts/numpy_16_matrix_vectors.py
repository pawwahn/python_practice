import numpy as np

a = np.array([(1,2,3),(2,3,4),(3,4,5)])
print a,"\n"
b = np.array([[(1,0,10)]])
print b,"\n"
c = a+b
print c,"\n"

z = np.array([[[(1,0,10,5),(1,5,4,5)]]])
print z,"\n"
print "shape",z.shape,"\n"
print "dim",z.ndim,"\n"

k =np.ones((3,3))
#print k,"\n"
k =np.zeros((3,3))
#print k,"\n"
z = np.arange(6,12)
z1 = z.reshape((6,1))
print "arange shape of matrix is ",z,"\n"
print "reshape matrix --> \n",z1



