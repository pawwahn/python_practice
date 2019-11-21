# def summy(*args):
#     for lst in args:
#         #print(lst)
#         print("****")
#         for key,value in lst.items():
#             print(key)
#             print(value)
#
# summy({'a':1},{'b':2},{'c':3},{'d':4})


def summy(lst):
    for lt in lst:
        #print(lst)
        print("****")
        for key,value in lt.items():
            print(key)
            print(value)

summy([{'a':1},{'b':2},{'c':3},{'d':4}])




