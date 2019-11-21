import numpy as np
a = np.array([[1,2,3,4,8,7,5,9,5,4,5,8],[1,2]])
print a.itemsize                                            # 8               
print a.shape           #(2,)

b = np.array([[1],[2,4]])
print b.itemsize        #8
print b.shape           # (2,)

c = np.array([[1,2,4,8,7], [4,5,5], [5,6,8],[1,7,8],[1],[]])
print c.itemsize        #8
print c.shape           # (6,)
print "*****",c.size    # 6

d = np.array([[1,2,3,4,8,7,5,9,5,4,5,8],[1,2],[0]])
print d.itemsize        #8
print d.shape           #(3,)

e = np.array([[[1,2,3,4,8,7,5,9,5,4,5,8]]])
print e.itemsize                                            # 8
print e.shape           #(1,1,12)

f = np.array([[[1,2,3,4,8,7,5,9,5,4,5,8],[1,2]]])
print f.itemsize                                            # 8
print f.shape           #(1,2)

g = np.array([[[[1,2,3,4,8,7,5,9,5,4,5,8],[1,2],[1,5]]]])
print g.itemsize                                            # 8
print g.shape           #(1,1,3)

h = np.array([[[[[1,2,3,4,8,7],[1,2],[1,5]]]]])
print h.itemsize                                            # 8
print h.shape           #(1,1,1,3)

i = np.array([[[[[[1,2,3,4,8,7],[1,2]],[1,5]]]]])
print i.itemsize                                            # 8
print i.shape           #(1,1,1,2,2)

j = np.array([[[[[1,2,3,4,8,7],[1,2],[[1,5]]]]]])
print j.itemsize                                            # 8
print j.shape           #(1,1,1,3)

k = np.array( [ [ [[1,2,3],[1,2],[3] ],[[1,2],[2]], [[1,2]] ]] )
print k.itemsize                                            # 8
print k.shape           #(1,3)
