# shallow copy
import copy
a = [1,2,3,4,5]
b = copy.deepcopy(a)
print a
print b
a[2] = 'pavan'
print a
print b
