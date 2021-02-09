class A(object):

    def __new__(cls, *args, **kwargs):
        print("Inside __new__")

    def __init__(self):
        print("inside Init")

    def func(self):
        print("Inside Func")

    @staticmethod
    def static_method():
        print("Inside Static method")

    def sample(self):
        print("sample")

a = A()
a.sample()
#a.static_method()      # no need to create object for calling the static method
A.static_method()