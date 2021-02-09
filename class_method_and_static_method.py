class DecoratorExample:
    """ Example Class """

    def __init__(self):
        """ Example Setup """
        print('Hello, World!')

    @staticmethod
    def example_function():
        """ This method is decorated! """
        print("example_function static method called --> ")

    def dummy_class(self):
        pass

    @staticmethod
    def new_dummy():
        print("new_dummy static method called --> ")

    @classmethod
    def new_class_func(cls):
        print("new_class_func called --> ")
        # cls.new_class_func()
        cls.new_dummy()


# de = DecoratorExample()
# de.example_function()
DecoratorExample.new_class_func()
