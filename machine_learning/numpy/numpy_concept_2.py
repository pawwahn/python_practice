#https://www.tutorialspoint.com/numpy/numpy_array_attributes.htm
import numpy as np

a = np.array([1,2,3,4,5,6])
print(a)

# this helps to make ndmin array
b = np.array([1,2,3,4,5],ndmin=2)
print(b)    # [[1 2 3 4 5]]

#create a complex numpy array by using dtype=complex
c = np.array([1,2,3,4,5,6],dtype=complex,ndmin=2)
print(c)

#find the shape of the numpy array created
d = np.array([[1,2,3,],[4,5,6]])
print(d,'\n')
print(d.shape,'\n')

#change the shape of existing numpy array
d.shape = (3,2)
print(d,'\n')


#numpy have other function which is reshape
print("Before reshape is above")
e = d.reshape(2,3)
print("after reshape is below")
print(e)