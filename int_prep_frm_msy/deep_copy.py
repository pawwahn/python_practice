# https://www.programiz.com/python-programming/shallow-deep-copy

import copy

old_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
new_list = copy.deepcopy(old_list)

print("Old list:", old_list)
print("New list:", new_list)

print("Id of old list is : {}".format(id(old_list)))
print("Id of new list is : {}".format(id(new_list)))