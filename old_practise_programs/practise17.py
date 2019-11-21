duplicates = ['a','b','c','d','d','d','e','a','b','f','g','g','h']
uniqueItems = list(set(duplicates))
print uniqueItems                       #    ['a', 'c', 'b', 'e', 'd', 'g', 'f', 'h']
print sorted(uniqueItems)               #   ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']