import numpy as np

a = np.array([[1,2,3,2],[9,1,3,4],[12,54,21,33]])
print(a)
print("\n")
print(np.sort(a))
print("\n")
print("axis=0")
print(np.sort(a,axis=0))
print("\n")
print("axis=1")
print(np.sort(a,axis=1))


