######
# Using OOP in Python, we can restrict access to methods and variables.
# This prevent data from direct modification which is called encapsulation.
# In Python, we denote private attribute using underscore as prefix i.e single “ _ “ or double “ __“.
#####

class Computer:
    __maxprice1 = 100

    def __init__(self):
        self.__maxprice = 900
        self.purchase_price = 750

    def sell(self):
        print("Selling Price: {}".format(self.__maxprice))
        # print("Selling Price: {}".format(self.__maxprice1))

    def purchase_price_method(self):
        print("Inside purchase price")
        print("Purchase Price: {}".format(self.purchase_price))

    def setMaxPrice(self, price):
        self.__maxprice = price


class Another_Computer(Computer):
    __maxprice1 = 1000


c = Computer()
c.purchase_price_method()
c.sell()

# print(c.__dict__)
# print(Computer.__dict__)

A = Another_Computer()
print(A._Another_Computer__maxprice1)
print(A._Computer__maxprice1)

# c._Computer__maxprice = 1000
# print(c._Computer__maxprice)
# # change the price
# c.__maxprice = 1000
# c.sell()
#
# # using setter function
# c.setMaxPrice(1000)
# c.sell()
