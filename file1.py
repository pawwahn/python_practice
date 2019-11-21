class MyClass:
    def f(self,name='abc'):
        print("f()")
        print(name)


def func(name):
    age = 0
    print(name)
    print(age)
func('Nandha')
func.age = 20
print(func.age)

func('Nandha')

