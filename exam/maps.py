lst = [1,2,3,4,5,6]

# map(lambda x : <your_function> , object)      ## to remember
print (map(lambda x: x**2,lst)) # result is obj

mp = map(lambda x: x**2,lst)
mp = set(mp)
print(mp)


def calculateSquare(n):
  return n*n

numbers = (1, 2, 3, 4)
result = map(calculateSquare, numbers)
print(result)

# converting map object to set
numbersSquare = set(result)
print(numbersSquare)




