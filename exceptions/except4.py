num = input("enter numerator")
den = input("enter denominator")
try:
    value = float(num)/float(den)
    print value
except IOError:
    print "IOException error..."
except KeyboardInterrupt:
    print "KeyboardError error..."
except ZeroDivisionError:
    print "ZeroDivisionError error..."
else:
    print "else in found error"

