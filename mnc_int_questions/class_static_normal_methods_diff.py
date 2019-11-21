class A:
    def __init__(self):
        print("<-- Inside init fucntion -->")
        #return True            # init can not return boolean

    @staticmethod
    def statMethod():
        print("<- Inside static method ->")
        #classmethod() # u can not cal a classmethod from static method
        #A().normalMethod()
        return "Stat Method"

    @classmethod
    def classMethod(cls):
        print("<- Inisde class method ->")
        #cls().normalMethod()   # u can call other functions available in the class ..
        #cls.statMethod()
        return "Class Method"


    def normalMethod(self):
        print("<- Inside normal method->")
        #self.statMethod()  # init will not be called, only stat gets called
        #A().statMethod()    # u have created obj, so init gets called and then statMethod gets called
        A.statMethod()
        #A.classMethod()
        return "Normal Method"

sm = A.statMethod()    # wen u call static method,_init_will not be called bcz we did not create obj A()
# sm = A().statMethod() # init gets called
#nm = A().normalMethod() # wen u call the normal method, init calls first
#cm = A().classMethod()    # wen u call the class method, init gets called
