import numpy as np

a = np.array([1,2,3])
print("The numpy array created is {}".format(a))
print("The numpy array type is {}".format(type(a)))
print("The length of numpy array is {}".format(len(a)))
print("The rank of numpy array is {}".format(np.ndim(a)))
print("*************")

b = np.array([(1,2,3),(4,5,6,7)])
print(b)
print("The numpy array type is {}".format(type(b)))
print("The length of numpy array is {}".format(len(b)))
print("The length of b[0] is {}".format(len(b[0])))
print("The length of b[1] is {}".format(len(b[1])))



'''
reasons for using numpy even as we have lists:
1. occupies less memory
2. fast to access
3. convenient to use

'''