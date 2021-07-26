privatclass A():
    a = "HI"

class B(A):
    print(A().a)

print(A.__dict__)
print(B.__dict__)


print(A().a)
#print(a)