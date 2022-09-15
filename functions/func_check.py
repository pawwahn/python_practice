
z = 3

def add_num(a,b):
    sm = True
    val = 'Sum only'
    k=a+b+z
    print(k)
    return sm,val

aaa = add_num(10,20)
print(aaa)

if aaa[0]==True:
    print(aaa[1])

x = -1

if x < 0:
    raise Exception("Sorry, no numbers below zero")