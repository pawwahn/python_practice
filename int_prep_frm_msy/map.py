a = input()

print(type(a))
print(a)

a = map(int, input().split())
print(type(a))
print(a)

a = list(map(int, input().split()))
print(type(a))
print(a)


def length(a):
    return len(a)

x = ['pavan', 'kumar', 'kota']

b = map(length, x)
print(tuple(b))