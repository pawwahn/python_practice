# find dimensions of array in numpy -- very important concept

import numpy as np

a = np.array([1,2,3])
print (np.ndim(a))
b = np.array([(1,2,3),(2,3,4)])
print (b.ndim)

#c = np.array([(1,2,3),(2,3),(1,2,3,4,6),(1,2,3)])
#print np.ndim(c)

c = np.array([(1,2,3),(2,3),(1,2,3,4,6),(1,2,3),(1,1,2),(1,2)])
print (np.ndim(c))

d = np.array([(1,2,3),(2,3,4),(1,4,5)])
print (d.ndim)


"""

[1,2,3] --- > dimension is 1 bcz it has only rows 

[(1,2,3),(2,3,4),(1,4,5)] --> dimension is 2 bcz it has both rows and columns

[(1,2,3),(2,3),(1,2,3,4,6),(4,5,6)]  --> dim is 1.Even it has both rows and columns, 
                    still it shows as 1 bcz the size in each row are not same to each other. so it treats as 1 object 
 

"""