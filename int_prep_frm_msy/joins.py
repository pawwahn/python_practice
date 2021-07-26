#list1 = ['1', '2', '3', '4']
##list1 = [1, 2, 3, 4]    #TypeError: sequence item 0: expected str instance, int found
a = [2,3,'a', 4,5]
c = 10
print(type(c))
#b = [i**2 for i in a]
# b = [i**2 for i in a if i.isdigit()]
# print(b)

list1 = "Hexaware"
s = "-"
s = s.join(list1)
# joins elements of list1 by '-'
# and stores in sting s


# join use to join a list of
# strings to a separator s
print(s)