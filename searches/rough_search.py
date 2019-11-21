my_sum = 7


def getSum(n):
    sum = 0
    # Single line that calculates sum
    while (n > 0):
        sum +=int(n % 10)
        n = int(n / 10)
    return sum

for i in range(0,100):
    a = getSum(i)
    if a==i:#my_sum:
        print(i)
        break
# print(i)

# a = getSum(100)
# print(a)