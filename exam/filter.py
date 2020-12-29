lists = [10, 20, 30, 40, 50, 60]
print (filter(lambda x: x > 20, lists))
x = filter(lambda x: x > 20, lists)
print(x)
print(tuple(x))

