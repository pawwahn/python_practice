#fibbonacci
k=[]
def fib(n):
    a,b = 0,1
    while(b<n):
        k.append(a)
        a,b=b,a+b
    return k
f = fib(10)
print(f)

# swap numbers with out using 3rd variable
a = 10
b = 20
a = a + b   #a ==> 10 + 20 = 30
b = a - b   #b ==> 30 - 20 = 10
a = a - b   #a ==> 30 - 10 = 20
print(a,b)