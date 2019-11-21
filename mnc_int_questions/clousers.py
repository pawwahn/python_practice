def a():
    print("Inside A")
    def b():
        print("Inside B")
    return b()

a()

def a1():
    a10 = "This is a1"
    def b10():
        print(a10)
    return b10()



a1()