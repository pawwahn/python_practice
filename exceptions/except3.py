num = input("enter numerator")
den = input("enter denominator")
try:
    value = float(num)/float(den)
    print (value)
except ZeroDivisionError:
    print ("ZeroDivisionError...")
except Exception:
    print ("exception 10Error...")
else:
    print ("else part2")
finally:
    print("inside finally")

