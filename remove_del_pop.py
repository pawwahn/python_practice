# del is a keyword and whereas remove and pop are python's inbuilt functions

# program to demonstrate use of del keyword

# assign list
numbers = [1, 2, 3, 2, 3, 4, 5]

# use del
del numbers[2]  # deletes the position element

# display list
print(numbers)

# use del
del numbers[-1]

# display list
print(numbers)

# use del
del numbers[0]

# display list
print(numbers)
print("############## Remove ##################")

# program to demonstrate use of remove() method

# assign list
numbers = [1, 2, 3, 2, 3, 4, 5]

# use remove()
numbers.remove(3)  #1st occured element will be removed

# display list
print(numbers)

# use remove()
numbers.remove(2)

# display list
print(numbers)

# use remove()
numbers.remove(5)

# display list
print(numbers)

# numbers.remove(50)      # throws error as 50 is not in the list
# print(numbers)

print("############## Pop ##################")
# pop() method returns deleted value from the list.

# program to demonstrate use of pop() method

# assign list
numbers = [1, 2, 3, 2, 3, 4, 5]

# use remove()
numbers.pop(3)

# display list
print(numbers)

# use remove()
numbers.pop(-1)

# display list
print(numbers)

# use remove()
numbers.pop(0)

# display list
print(numbers)
