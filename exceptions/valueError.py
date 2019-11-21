lst = [1,2,3,4,5,6,7]

try:
    a,b,c = lst
except AssertionError as a:
    print a
except ZeroDivisionError as z:
    print z
except ValueError as e:
    print e