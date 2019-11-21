class Singleton:
   __instance = None


   @staticmethod
   def getInstance():
      """ Static access method. """
      print("Inside getInstance method")
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance


   def __init__(self):
      """ Virtually private constructor. """
      print("Inside __init__ method")
      if Singleton.__instance is not None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self

s = Singleton()
print(s)

s = Singleton.getInstance()
print(s)

s = Singleton.getInstance()
print(s)

t = Singleton.getInstance()
print(t)