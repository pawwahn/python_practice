class Foo:
    def __init__(self,a,b):
        print("Inside Init")
        self.a = a
        self.b = b

    def __call__(self,a,b):
        print("Inside call method")
        return a+b

    def dummy_func(self):
        print("Inside dummy class")

f = Foo(10,20)


f('hello','world') # This invokes the __call_  # comment this and run and uncomment and run
f.dummy_func()
