a = [1, 2, 3, 4, 2, 3, 4, 5, 1, 2, 3]

b = list(set(a))
print(b)
dict ={}

for i in b:
    dict[i] = a.count(i)

print(dict)

