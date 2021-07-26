class A:
    __default_value=1000
    def __init__(self):
        self.a = 10
        self.__A = 100


    # def __private(self):
    #     print("Inside private")
    #     print(self.a)
    #     print(self.__A)

    def normal(self):
        print("Inside normal method")
        print(self.__default_value)
        self.__default_value=200
        print(self.__default_value)


#print(__default_value)
a= A()
a.normal()
#A()._A__private()
