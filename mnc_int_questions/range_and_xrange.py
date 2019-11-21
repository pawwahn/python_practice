# Python code to demonstrate range() vs xrange()
# on  basis of return type

# initializing a with range()
a = range(1, 10000)

# initializing a with xrange()
x = xrange(1, 10000)   # xrange is not available in 3

# testing the type of a
print("The return type of range() is : ")
print(type(a))

# testing the type of x
print("The return type of xrange() is : ")
print(type(x))