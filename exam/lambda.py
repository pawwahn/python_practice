
tot = lambda x,y: x+y
print (tot(10,20))

exp = lambda x: 3*x + 1
print (exp(3))

names  = lambda fn,ln : str(fn.strip().title()) + " "+ str(ln.strip().title())
print (names("    pavan","    kota   "))

sub = lambda a,b: b-a
print(sub(10,20))

strip_string = lambda strip_str : str(strip_str.strip())
print(strip_string("       pavan            "))

k=[1,2,3]
def sqs(k):
    for i in k: return i*i

sqrs = lambda x:sqs(k)
print(sqrs(k))