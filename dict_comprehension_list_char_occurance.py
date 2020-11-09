a = [1, 2, 3, 4, 2, 3, 4, 5, 1, 2, 3]
b = list(set(a))

dict = {}

new_dict = {i: a.count(i) for i in b if i in a}
print(new_dict)