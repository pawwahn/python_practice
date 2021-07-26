a = [1,2,3,4,5,6,7,8,9,0]
#print(a.__next__())
print(type(a))

a.iter()
itr = iter(a)

print(a.__next__())

print (itr)
print (next(itr))
print (next(itr))
print(a.__sizeof__())