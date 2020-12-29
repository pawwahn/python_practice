class A:
    def __init__(self):
        print("<-- Inside init fucntion -->")

    @staticmethod
    def statMethod():
        print("<- Inside static method ->")
        #classmethod() # u can not cal a classmethod from static method
        #A().normalMethod()
        return "Stat Method"

    @classmethod
    def classMethod(cls):
        print("<- Inisde class method ->")
        return "Class Method"


    def normalMethod(self):
        print("<- Inside normal method->")
        A.statMethod()
        return "Normal Method"

#sm = A.statMethod()
# wen u call static method,_init_will not be called bcz we did not create obj A()
#sm = A().statMethod() # init gets called
# nm = A().normalMethod() # wen u call the normal method, init calls first
#cm = A().classMethod()    # wen u call the class method, init gets called
A().classMethod()
