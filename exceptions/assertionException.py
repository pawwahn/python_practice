

num1 = int(input("enter a"))
num2 = int(input("enetr b"))

def test(a,b):
    assert a>b," condition fails"

try:
    test(num1,num2)
    print "does not raise exception as a is greater than b"
except Exception as e:
    print e

