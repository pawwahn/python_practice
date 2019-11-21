"""
in numpy array, give the index values as given below(index) and u can easily find out the values of the other array(a)'s values  

"""
#'''
"""
the below code works as this is not list and is a numpy array
"""
import numpy as np

a = np.array([0,1,2,3,4,6,7,8])
index = [2,5,6,]

print a[index]
print type(a[index])
#'''

''' 
"""
the below code will not work bcz lst is list
"""
lst = [0,1,2,3,4,5,6,7]
ind = [1,3,4]
print lst[ind]
'''