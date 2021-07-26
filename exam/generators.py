
#ques
def remote_control():
    yield "AXN"
    yield "HBO"
    yield "CNN"

#ans
a = remote_control()
print(next(a))
print(next(a))
print(next(a))
#print(next(a))