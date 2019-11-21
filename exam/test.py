def square(x):
    return x*x

def my_func(func,list_args):
    result = []
    for i in list_args:
        result.append(func(i))
    return result

squares = my_func(square,[1,2,3,4,5])
print squares