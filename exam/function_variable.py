def a():
    a.var = 100
    print(a.var)

def b():
    print(a.var)

a()
b()

print(a.var)