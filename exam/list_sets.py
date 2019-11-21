lst = [1,2,3,4,1,2,3,4]
print (lst)
lst.sort()
print (lst)
lst.sort(reverse=True)
print (lst)
#print rev_list
#x = set(lst)
x = set([1,2,3,1,2,3,1,2,3,4,5,6,7])
print("set--->>>",x)
y = x.copy()
print (y.difference(lst))

# extend
a=[1,3,5]
b = ['a','b']
a.extend(b)
print ("extend",a)

# append
i = [1,3,5]
j = ['a','b']
i.append(j)
print ("append",i)

