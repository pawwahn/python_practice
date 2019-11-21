import copy

#shallow copy
a = [1,2,3,4,5]
b = copy.copy(a)
print a
print b
a[2] = 'pavan'
print a
print b
