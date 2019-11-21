import numpy as np

a = np.array([[4, 5, 6], [7, 8, 9], [1, 2, 13], [12, 11, 10], [1, 1, 1], [10, 11, 12]])
print(a)

print('Applying amin() function:')
print(np.amin(a))
print(np.amin(a, 0))
print(np.amin(a, 1))
print("<--Min axis 0 and axis 1-->")
print(np.amin(a, axis=0))
print(np.amin(a, axis=1))

print('Applying amax() function:')
print(np.amax(a))
print(np.amax(a, 0))
print(np.amax(a, 1))
print('Applying amax() function again:')
print(np.amax(a, axis=0))
print(np.amax(a, axis=1))

#The numpy.ptp() function returns the range (maximum - minimum) of values along an axis.

print('Applying ptp() function:')
print(np.ptp(a))
print('\n')

print('Applying ptp() function along axis 1:')
print(np.ptp(a, axis = 1))
print('\n')

print('Applying ptp() function along axis 0:')
print(np.ptp(a, axis = 0))

