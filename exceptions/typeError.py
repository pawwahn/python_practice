a = 10
b = 100
try:
    c = a+b
    f = open("dummys.csv")
except ZeroDivisionError as z:
    print "ZeroDivisionError -->",z
except TypeError as t:
    print "TypeError --> ",t
except NameError as n:
    print "NameError --> ",n
except IOError as n:
    print "IOError --> ",n
except Exception as e:
    print "Exception --> ",type(e).__name__