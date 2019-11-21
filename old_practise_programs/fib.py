def fib(n):
    a,b = 0,1
    while n>a:
        print a
        a,b = b,a+b
    return True

fib(100)