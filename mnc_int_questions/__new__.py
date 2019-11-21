class A(object):  # -> don't forget the object specified as base

    # def __new__(cls):
    #     print ("A.__new__ called")                                    # cls obj parameter also works
    #     return super(A, cls).__new__(cls)

    def __new__(self):
        print("A.__new__ called")
        return super(A, self).__new__(self)                 # __new__ should be callable

    def __init__(self):
        print("A.__init__ called")

    def __call__(self):
        print("Call called")

a = A()
a()