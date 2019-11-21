class DecoratorExample:
    """ Example Class """

    def __init__(self):
        """ Example Setup """
        print('Hello, World!')

    @staticmethod
    def example_function(a,b):
        """ This method is a static method! """
        print('I\'m a static method!')
        print(a+b)
        return "Static Function"

    def normal_function(self,a,b):
        print("This is a normal function")
        print(a+b)
        return "Normal Function"

sm = DecoratorExample.example_function(5,4)        # no need to create object
print("----------")
nm = DecoratorExample().normal_function(10,20)       # need to create object



