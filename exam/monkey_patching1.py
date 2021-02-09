class MonkeyPatching:
    def __init__(self):
        print("Inisde Init")

    def f1(self):
        print("Inside f1")

    def f2(self):
        print("Inside f2")
        self.f1()

mp1 = MonkeyPatching()
mp1.f1()
# mp1.f2()

def OutSideMonkeyPatching(self):
    print("Out of monkey patching")

MonkeyPatching.f1 = OutSideMonkeyPatching
print("outside line of monketpatching")

mp2 = MonkeyPatching()
mp2.f1()
mp2.f2()