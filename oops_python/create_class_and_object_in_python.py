class Parrot:
    # class attribute
    species = 'bird'

    #instance attribute
    def __init__(self,name,age):
        self.name = name
        self.age = age

#instantiating the class
blu = Parrot("blu",5)

#prints the class object
print(blu)

# 1st way of retriving class attribute
print(Parrot.species)

#2nd way of retriving the class attribute,
print(blu.__class__.species)

#retrive object attributes
print(blu.name)