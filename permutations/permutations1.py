import itertools
from itertools import permutations

list1 = ['1', '2', '3', '4', '8', '5', '2']
list2 = ['4', '2', '5', '6', '8', '7', '4']

def print_values(map_object):
    for i in map_object:
        print(1)


#map_object = map(''.join, itertools.chain(itertools.product(list1, list2), itertools.product(list2, list1)))
c = map(''.join, itertools.chain(itertools.product(list1, list2), itertools.product(list2, list1)))
print(list(c))

#print_values(map_object)


