class Parrot:

    #class attribute
    species = 'bird'

    #instance attribute
    def __init__(self,name,age):
        self.name = name
        self.age = age

    #instance method
    def sing(self,song):
        return "{} sings {} song".format(self.name,song)

    # instance method
    def dance(self):
        return "{} is now dancing".format(self.name)

#instantiating object
blu = Parrot("kuku",10)

#retrive class attribute
print(blu.__class__.species)

#retrive instance values
print(blu.name)
print(blu.age)

#call instance method
blu_song = blu.sing("jum jum maya")
print(blu_song)

#call instance method
blu_dance = blu.dance()
print(blu_dance)

