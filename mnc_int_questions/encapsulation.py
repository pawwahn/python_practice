class A:
    __default_price=10
    def __init__(self):
        print("Inside init func")
        self.__max_price = 100
        self.a = "a value is accessed as it is not private varible"

    def sell(self):
        print("selling price is: {}".format(self.__max_price))

    def find_default_price(self):
        print("default selling price is: {}".format(self.__default_price))

    def __privatef(self):
        print("------ Inside private")

a = A()
a.sell()
#print(A().__default_price)  # we can't access private class varibles by creating obj,they can b called only inside the func
a.find_default_price()
print(a.a)
print(A()._A__privatef())