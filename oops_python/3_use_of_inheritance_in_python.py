#parent class
class Bird:
    def __init__(self):
        print("Bird is ready")

    def whoisThis(self):
        print("Bird")

    def swim(self):
        print("Bird swims")

    def walk(self):
        print("Bird walks")

    def sleep(self):
        print("Bird is sleeping")

#child class

class Duck(Bird):
    def __init__(self):
        #call super() function
        super().__init__()      #this is the line to call the parent __init__ method
        print("Duck is ready")

    def whoisThis(self):
        super().whoisThis()
        #print("Duck")      #it also works

    def run(self):
        print("Run faster")

    def swimming(self):
        print("Duck is swimming")

    def walk(self):
        print("Duck is walking")

dk = Duck()
dk.whoisThis()

# the below line shows AttributeError
#dk.swim()  #AttributeError: 'Duck' object has no attribute 'swim'

dk.run()    #Run faster

dk.walk()   #Duck is walking

dk.sleep()  #Bird is sleeping as child class does not have the method sleep. so, as child inherits from parent, it calls the sleep() in the parent class

dk.swimming()   #Duck is swimming




