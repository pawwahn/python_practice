l = [1,2,3,4,5]
result = [x**2 for x in l]
print (result)

a = [1,2,3,4]
res = [(i*3) for i in a]
print (res)

b = [10,20,30,40,50,60,70,80,90]
res = [(i*2) for i in b if i>50]
print (res)

lists = [1,2,5,3,6,4,8,9]

lc = [(i**2) for i in lists]
print (lc)

a = [1,2,3]
for b in a:
    print(b*b)

b = [10,20,30]
x = [(i*i) for i in b]
print(x)

bi = [10,20,30]
x = [(i*i) for i in bi if i >25]
print(x)

bie = [10,20,30]
x = [(i**3) for i in bie if i >25]
print(x)