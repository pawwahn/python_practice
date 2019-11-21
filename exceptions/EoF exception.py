num1 = raw_input("enter num1")
num2 = raw_input("enter num2")

def test(num1,num2):
    if num1 > num2:
        print "true"
    else:
        print "false"

try:
    test(num1,num2)
except EOFError as e:
    print e