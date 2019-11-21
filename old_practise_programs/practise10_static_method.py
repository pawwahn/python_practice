class Car(object):

    wheels = 4

    def __init__(self, make, model):
        self.make = make
        self.model = model
        fun = self.fun()

    def fun(self):
        print("funct**")

mustang = Car('Ford', 'Mustang')
print ()
# 4
print (Car.wheels)

car2 = Car('BMW','Q5')
print (car2.make)
car2.wheels = 5
print ("car2 wheels count",car2.wheels)
print ("Mustang wheels count",mustang.wheels)