"""
Q-7. Can you write code to determine the name of an object in Python?

Ans. No objects in Python have any associated names. So there is no way of getting the one for an object. 
    The assignment is only the means of binding a name to the value. 
    The name then can only refer to access the value. The most we can do is to find the reference name of the object.
"""


class Test:
    def __init__(self, name):
        self.cards = []
        self.name = name
 
    def __str__(self):
        return '{} holds ...'.format(self.name)
        
obj1 = Test('obj1')
print obj1
 
obj2 = Test('obj2')
print obj2