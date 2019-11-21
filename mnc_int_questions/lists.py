l = [1,2,3]
m = [10,20]

p = [4,5,7]
q = [40,50,60,40,40,40,40]

# type of l
print("Type is: {}".format(type(l)))

#slicing
print("slicing {}".format(l[1:]))

#last element
print("Last element is: {}".format(l[-1]))

#append
l.append(m)
print("After appending: {}".format(l))
print("M: {}".format(m))

#extend
p.extend(q)
print("P after extending with q is: {}".format(p))
print("Q remains the same as : {}".format(q))

#insert
print("Before inserting element to list P: {}".format(p))
p.insert(2,6)
print("List P after inserting :{}".format(p))

# pop
p.pop(2)
print("After Pop with index 2, the elements are as follows :{}".format(p))

#remove -- it removes the 1st object
p.remove(40)
print(p)

#count -- input the value to be counted, it returns the no. of elements found in the object
cnt = p.count(40)
print(cnt)

print("Length of list p is: {}".format(len(p)))

