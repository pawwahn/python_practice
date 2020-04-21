e = {1:1, 2:2, 3:3, 4:4}
d1 = {'a':1,'b':2,'c':3,'d':4}

for i in e:
    print(i)    # d c a b

d10 = {'a':1,'b':2,'c':3,'d':4}

new_d1 = {x:y**2 for x,y in d10.items()}
print(new_d1)