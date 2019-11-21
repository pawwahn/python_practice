class A():
    # print("in class a")
    def __init__(self):
        print("Inside A class init")

    def run(self):
        print("Inside A run")

    def walk(self):
        print("Inside A walk")

class B(A):
    # print("in class b")
    def __init__(self):
        print("Inside B class init")

    def run(self):
        print("Inside B run")

    def swim(self):
        print("Inside B swim")

#class C(A,B):  #TypeError: Cannot create a consistent method resolution  --> 1st checks A class and den goes to B and then A.. so, this is wrong
class C(B, A):
    # print("in class c")
    def __init__(self):
        print("Inside C class init")

    def swim(self):
        print("Inside C swim")

obj1 = C()
obj1.run()
print(C.__dict__)
if 'swim' in C.__dict__:
    print(True)
    #C.Name = 'Nandha'
print(obj1.__dict__)
print(C.__dict__)