a,b = 10,10
try:
    c = a/b
    #file = open('no_file.txt')
    x,y = 10,"pavan"
    z=x+y
except ZeroDivisionError as e:
    print "Zero Division Error",e
except IOError as e:
    print "IOError or file not found"
except TypeError as e:
    print "Type error occured",e
except AssertionError as e:
    print "Assertion Exception",e
else:
    print "Inside else block"
    #z = x+y
finally:
    print "It runs always"