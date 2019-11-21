import copy

list1 = [1,2,3,4,5]
print(list1)

list2 = copy.deepcopy(list1)
print(list2)

list1[2] = 'a'


print("<-- In deep copy, if list1's value is changed, It does not show the change in list2 --> ")
print(list1)
print(list2)

print("***********************************")

a = [1,2,3,4,5]
print(a)

b = copy.copy(a)
print("b is {}".format(b))

a[2] = 'pavan'
print("a is {}".format(a))
print("b is {}".format(b))


