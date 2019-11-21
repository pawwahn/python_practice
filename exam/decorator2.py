###########   code duplication #############
# def print_name():
#     print "just entered in to the function"
#     print "Pavan"
#     print "At the end of the fumction"
#
# def print_city():
#     print "just entered in to the function"
#     print "chennai"
#     print "At the end of the fumction"
########## code duplication #############

def my_decorator(func):
    def wrapper():
        print ("Just Entered in to the function")
        func()
        print ("At the end of the function")
    return wrapper

@my_decorator
def print_name():
    print ("Pavan")

@my_decorator
def print_city():
    print ("Chennai")

print_name()
print_city()