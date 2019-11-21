def myFun(a):
    return a.upper()

x = map(myFun, ['apple','mango','carrot'])
print(map)
print(list(x))
print("-----------------")


def myfun(a):
    return len(a)

x = map(myfun, ['apple','mango','carrot'])
print(map)
print(list(x))

print("------------>>>>>>>>>")
def myfun(a):
    sum=0
    for i in a:
        sum = sum+i
    return sum

x = map(myfun, [(1,2),(2,3),(4,5,8)])
print(list(x))

