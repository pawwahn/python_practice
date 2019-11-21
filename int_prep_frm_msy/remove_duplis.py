duplicates = ['a','b','c','d','d','d','e','a','b','f','g','g','h']
uniqueItems = set(duplicates)
print(uniqueItems)  # results in {} braces
uniqueItems = list(set(duplicates)) # results as a list []
print (sorted(uniqueItems))