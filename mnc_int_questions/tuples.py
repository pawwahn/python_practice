tup1 = (1,2,3,[10,20,30],{1:1,2:2,3:3})
tup2 = (10,20,30)

print(" Type {}".format(type(tup1)))
print(" Type of 3rd element in the tuple is: {}".format(type(tup1[3])))

#tup1[3]=[4]        # TypeError: 'tuple' object does not support item assignment
#print(tup1)

print(tup1[3])
tup1[3][0]=100
tup1[3][1]=200
tup1[3][2]=300
#tup1[3][4]=[400]

print(tup1) #(1, 2, 3, [100, 200, 300])
print("slicing: {}".format(tup1[2:]))

print("count of 3 in tuple is: {}".format(tup1.count(3)))

print(tup1.__contains__(1))
print(tup1.__getitem__(4))





