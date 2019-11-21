class Parrot:

    def fly(self):
        print("Parrot can fly")

    def swim(self):
        print("Parrot can't swim")


class Penguin:

    def fly(self):
        print("Penguin can't fly")

    def swim(self):
        print("Penguin can swim")

#common interface
def flying_bird(bird):
    bird.fly()

par = Parrot()
# par.swim()
# par.fly()

flying_bird(par)

pen = Penguin()
flying_bird(pen)