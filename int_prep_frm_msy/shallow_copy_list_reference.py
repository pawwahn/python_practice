import copy

old_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
new_list = copy.copy(old_list)

old_list[1][1] = 'AA'

print("Old list:", old_list)
print("New list:", new_list)

print("Id of old list is : {}".format(id(old_list)))
print("Id of new list is : {}".format(id(new_list)))

print("Id of old_list[1][1] is : {}".format(id(old_list[1][1])))
print("Id of new_list[1][1] is : {}".format(id(new_list[1][1])))



#In the above program, we made changes to old_list i.e
# old_list[1][1] = 'AA'. Both sublists of old_list and
# new_list at index [1][1] were modified.
# This is because, both lists share the reference of same nested objects.

# ids are different but still list value changes