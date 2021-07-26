# #Simple Iteration
# item = []
# for n in range(10):
#     item.append(n*2)
# print (item)
#
# #listComprehension
#
# item = [n*2 for n in range(10)]
# print(item)

a = [1,2,3,4,5,'a',20]

print([i*i for i in a if type (i)==int])