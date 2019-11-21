class A:
    def sayhi(self):
                    print("I'm in A")
class B(A):
    def sayhi(self):
        #super().sayhi()
        print("I'm in B")
bobj=B()
bobj.sayhi()