lst1 = ['a','b','c','d','e']
lst2 = [1,2,3,4,5]
a = zip(lst1,lst2)
print("--*>",a)
a = set(a)
print(a)
# for i in a:
#     print(i[0])
#     print(i[1])

i = 0
dict = {}
for lst in lst1:
    dict[lst] = lst2[i]
    i+=1

print(dict)
