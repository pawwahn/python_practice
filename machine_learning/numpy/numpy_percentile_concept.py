import numpy as np

#a = np.array([[np.arange(0,9,2)],[np.arange(10,19,2)]])
a = np.array([[10, 20, 25, 30, 40, 50, 55, 55, 65, 80, 85, 90]])
print(a)
#print((75/100)*12)
#print(np.shape(a))


#print(np.percentile(a, 75))
print("<--mean-->")
print("Mean is the average")
print(np.mean(a))
print("<--median-->")
print("Median is the middle number")
print(np.median(a))
print(np.median(a,axis=0))
print(np.median(a,axis=1))

