import time
def time_it(f):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = f(*args,**kwargs)
        end = time.time()
        print ("The time take is: "+ str((end-start)*1000)+" milli sec")
        return result
    return wrapper

array = range(1,100)

#print array

@time_it
def calc_square(numbers):
    result = []
    for num in numbers:
        result.append(num*num)
    return result

@time_it
def calc_cube(numbers):
    result = []
    for num in numbers:
        result.append(num*num*num)
    return result

out_cube = calc_cube(array)
out_square = calc_square(array)