ls1 = ['a','b','c','d','e','f']
ls2 = ['q','w','e','r','t','y','u']

obj1 = enumerate(ls1)
obj2 = enumerate(ls2)

print(obj1)
print(obj2)

print(list(obj1))
print(list(enumerate(ls2)))

print(list(enumerate(ls2,100))) # parameter b, which is given as 100 is for setting the starting value


