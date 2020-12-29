class First:
    def __init__(self):
        print("first")

class Second(First):
    def __init__(self):
        super().__init__()
        print("second")

class Third(Second,First):
    def __init__(self):
        #super(Third,self).__init__()
        super().__init__()
        print("third")

Third()
