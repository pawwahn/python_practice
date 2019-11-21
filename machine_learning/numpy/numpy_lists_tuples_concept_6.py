import numpy as np

print("<-- list and tuple float type-->")
x,y = [1,2,3],(4,5,6)       # list and tuple
q = np.array(x,dtype=float)
r = np.array(y,dtype=float)
print(q)
print(r)
print("<-- list and tuple int type-->")
q = np.array(x,dtype=int)
r = np.array(y,dtype=int)
print(q)
print(r)
print("combination of both list and tuple with int type -->")
z = [(1.99999,2,3),[4,5,6],(7,8.2,9.9)]       # float value also changes to int
z1 = np.array(z,dtype=int)
print(z1)

print("combination of both list and tuple with float type -->")
z = [(1.99999,2,3),[4,5,6],(7,8.2,9.9)]       # int value also changes to float
z1 = np.array(z,dtype=float)
print(z1)
