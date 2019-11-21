# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(N):
    for i in range(N, 1000):
        sum = 0
        n=i
        while (n > 0):
            sum += int(n % 10)
            n = int(n / 10)
        if sum == N:
          return i

a= solution(7)
print(a)


