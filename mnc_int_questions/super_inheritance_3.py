class A(object):

    def __init__(self):
        print("Inside A inheritance")

class B(object):
    def __init__(self):
        print("Inside B inheritance")

class C(A, B):
    def __init__(self):
        print("Inside C inheritance")
        super().__init__()

obj = C()