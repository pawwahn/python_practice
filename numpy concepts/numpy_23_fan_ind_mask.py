import numpy as np

#a = np.arange(12).reshape(4,3)
a = np.array([(1,2,3,4),(2,3,4,5),(3,1,2,1)])
print(a,"\n")

j = a[(a-3) < 2]
print(j,"\n")

j = a[abs(a-3) < 2]
print(j,"\n")

p = a.sum(axis=0)
print("sum of p",p,"\n")

q = a.sum(axis=1)
print("sum of q",q,"\n")


s = a[a.sum(axis=1) > 9, 1:]            # very imp concepts of numpy
print("sum of s \n",s)

