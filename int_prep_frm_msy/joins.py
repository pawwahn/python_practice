list1 = ['1', '2', '3', '4']
##list1 = [1, 2, 3, 4]    #TypeError: sequence item 0: expected str instance, int found

list1 = "pavan"
s = "-"

# joins elements of list1 by '-'
# and stores in sting s
s = s.join(list1)

# join use to join a list of
# strings to a separator s
print(s)