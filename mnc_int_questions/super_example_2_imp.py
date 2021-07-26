class First(object):
    def __init__(self):
        print ("First Init")

class Second(object):
    def __init__(self):
        print ("Second Init")

class Third(First, Second):
    def __init__(self):
        super(Third, self).__init__()
        print ("Third Init")

Third()