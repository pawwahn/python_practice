import copy
li1 = [1, 2, [3,5], 4]
li2 = copy.deepcopy(li1)

print ("The original elements before deep copying")
for i in range(0,len(li1)):
    print li1[i]
 
li2[2][0] = 7
print ("The original elements of deep copy")
for i in range(0,len(li2)):
    print li2[i]
    
print ("The original elements after deep copying is")
for i in range(0,len(li1)):
    print li1[i]
    
    
""" ******************        shallow copy below code            ***********"""


print "shallow copy code below **"
li1 = [1, 2, [3,5], 4]

# using copy to shallow copy
li2 = copy.copy(li1)

# original elements of list
print ("The original elements before shallow copying")
for i in range(0,len(li1)):
    print (li1[i])

# adding and element to new list
li2[2][0] = 7

# checking if change is reflected
print ("The original elements after shallow copying")
for i in range(0,len( li1)):
    print (li1[i])