x = {'a':1, 'b':2}
y = {'q':3, 'w':2}

z = {**x, **y}              # very imp concept
print(z)
print(*x)
print(*y)
print(x.keys())

print(*x.values())