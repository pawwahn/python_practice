class Vehicle:
    def __init__(self):
        print ("Inside init method of vehilce")

    def runs(self):
        print ("Runs as vehicle")

class Bike(Vehicle):

    def __init__(self):
        print ("Inside init method of Bike")
        super().__init__()

    def wheels(self):
        print ("Has 2 wheels")

class Car(Vehicle):

    def wheels(self):
        print ("Has 4 wheels")

    def runs(self):
        print ("Runs as Car")

c = Car()
b = Bike()
b.wheels()
# c.wheels()
# c.runs()