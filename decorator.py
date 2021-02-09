def time_its(func):
    def wrapper(*args,**kwargs):
        print("Line 1")
        result = func(*args,*kwargs)
        print(result)
        print("Line 2")
        print("\n")
        return result
    return wrapper

@time_its
def cal_square(number1,number2):
    result = number1*number2
    return result

@time_its
def cal_cube(number1,number2,number3):
    result = number1*number2*number3
    #print(result)
    return result

out_square = cal_square(10,5)
out_cube = cal_cube(10,20,30)

# def my_deco(f):
#     def wrapper():
#         print("Line1")
#         f()
#         print("Line2")
#         return wrapper
#
# @my_deco
# def print1():
#     print("Kota")
#
# @my_deco
# def print2():
#     print("Pavan")



