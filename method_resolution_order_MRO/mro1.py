class A:
    def process(self):
        print('A process()')

class B:
    pass

class C(A, B):
    pass


obj = C()
obj.process()
print(C.mro())