num = input("enter numerator")
den = input("enter denominator")

def test(a,b):
    if a > b:
        return a+b

try:
    a = test(num,den)
    print a
except FloatingPointError as f:
    print f
except EOFError as e:
    print e
