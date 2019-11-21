def adder(a, b):
    print(a,b)
    return a + b

def caller(fun):
    print(fun(2, 4))
    print(fun(3, 5))

caller(adder)