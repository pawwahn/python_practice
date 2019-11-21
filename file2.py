import file1


def monkey_f(self,name='xyz'):
    print("monkey_f()")
    print(name)


file1.MyClass.f = monkey_f
obj = file1.MyClass()
#print(obj)
obj.f()