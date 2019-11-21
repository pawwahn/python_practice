def my_dec(func):
    print(func)
    def wrapper(*args,**kwargs):
        print("Line Number 1")
        func(*args,**kwargs)
        print("Line Number 3")
    return wrapper


@my_dec
def square(number):
    print (number*number)

@my_dec
def cube(number):
    print (number*number*number)

cube(3)
square(2)

