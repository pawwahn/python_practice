import numpy as np

arr = np.array([1,2,3,4,5,6,7])
print arr

mask = np.array([True,False,False,True,True])

print mask

k = arr[mask]                       # masking is to find out 'true values'('one of the conditions') i.e, 
                                    # compare 2 arrays and gives the values which are true in position with the other array. 
print k

#mask1 = ((arr <2) | (arr >4))
#print arr(mask1)
