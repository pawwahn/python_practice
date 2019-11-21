n = 25
def fact(n):
    factorial = 1
    for i in range(1,n + 1):
           factorial = factorial*i
    return factorial

fct = fact(25)
print(fct)
# 5 * 4 * 3 * 2 * 1==