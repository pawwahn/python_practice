class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

o1 = Singleton()
print(o1)
print(id(o1))
o1.data = 10
print(o1.data)


o2 = Singleton()
print(o2)
print(id(o2))
print(o2.data)
o2.data = 20
print(o1.data)
print(o2.data)