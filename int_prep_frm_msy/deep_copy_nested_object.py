#https://www.programiz.com/python-programming/shallow-deep-copy

import copy

old_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
new_list = copy.deepcopy(old_list)

old_list[1][0] = 'BB'

print("Old list:", old_list)
print("New list:", new_list)

print("Id of old list is : {}".format(id(old_list)))
print("Id of new list is : {}".format(id(new_list)))

print("Id of old_list[1][1] is : {}".format(id(old_list[1][1])))
print("Id of new_list[1][1] is : {}".format(id(new_list[1][1])))

print("Old list:", old_list)
print("New list:", new_list)