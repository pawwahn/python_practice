import time

def my_decorator(func):
    def wrapper(*args,**kwargs):
        print(*args)
        print("---")
        print(**kwargs)
        start = time.time()
        func(*args,**kwargs)
        end = time.time()
        print ("Time take by "+ func.__name__ +" is "+ str((end - start) * 1000) + "ms")
    return wrapper
array = range(1,10000)

@my_decorator
def calc_square(numbers):
    result = []
    for num in numbers:
        result.append(num * num)
    return result

@my_decorator
def calc_cubes(numbers):
    result = []
    for num in numbers:
        result.append(num * num * num)
    return result

calc_square(array)
calc_cubes(array)