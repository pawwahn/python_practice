import numpy as np

#numpy.empty function
#'C' for C-style row-major array, 'F' for FORTRAN style column-major array


a = np.empty([2,3],dtype=float, order='C')
print(a)
print("**------->>")
b = np.empty([2,3],dtype=int, order='C')
print(b)
print("**------->>")
c = np.empty([2,3],dtype=int, order='F')
print(c)

######np.zeros######

d = np.zeros([3,4])
print(d)
print("####>>")
e = np.zeros(5)
print(e)

# fot integer zero
print("Integer zeros below..")
e = np.zeros(6, dtype=int)
print(e)






