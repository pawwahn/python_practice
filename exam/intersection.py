a = ['1','2','3']
b = ['1','2']
c = {'4','1'}
print(type(c))

new_a = set(a)
new_b = set(b)
# print(type(new_a))

print(new_a.intersection(new_b,c))