#shallow copy


import copy

old_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
new_list = copy.copy(old_list)

old_list.append([4, 4, 4])

print("Old list:", old_list)
print("New list:", new_list)

print("Id of old list is : {}".format(id(old_list)))
print("Id of new list is : {}".format(id(new_list)))