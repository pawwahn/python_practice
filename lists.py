a = []
print(a)
print(type(a))

b = [1,2,3]
print("length of b is: {}".format(len(b)))

c = [{'a':1,'b':2}]
print("length of dictonary c is: {}".format(len(c)))

d = [{'a':1},{'b':2},{}]
print("length of d is: {}".format(len(d)))

a = [1,2,3]
print("The value of a is: {}".format(a))

a.extend([4,5,6])
print("The extended value of a is : {}".format(a))

##loops##
b = [1,2,3]
for i in b:
    print(i)

j=0
c = ['a',[1,2,3],{'a':1,'b':2},10]
for i in c:
    j=j+1
    print("The {}th element is {}:".format(j,i))

#append
a = [1,2,3]
print("The List before appending is : {}".format(a))
a.append([2,3])
print("The List after appending is : {}".format(a))

#specific element
print("The 2nd element is '{}'".format(a[2]))

#negative indexing
a = [1,2,3,4,5]
print("The negative index is : {}".format(a[-1]))
print("The negative index is : {}".format(a[-2]))

#slicing
a = [1,2,3,4,5]
print("The slicing is : {}".format(a[:3]))
print("The slicing is : {}".format(a[:-1]))
print("The slicing is : {}".format(a[1:2]))


#update list
a = [1,2,3,4,5]
print("The 0th element before updating is : '{}'".format(a[0]))
a[0]='a'
print("The 0th element before updating is : '{}'".format(a[0]))

#shuffel
from random import shuffle
a = [100,1,40,2,3]
a.sort(reverse=True)
print(a)
a.sort()
print("sorted list :{} -- line 63".format(a))
a = "Pavan Kumar"
print(a[2:5])
print(a[::-1])