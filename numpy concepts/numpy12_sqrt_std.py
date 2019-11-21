import numpy as np

a = np.array([(1,2,3),(2,3,4),(4,3,2)])
mean = np.mean(a)
print (mean,"mean ")

print("sqrt of the array is \n",np.sqrt(a),"\n")

"""
[[ 1.          1.41421356  1.73205081]
 [ 1.41421356  1.73205081  2.        ]
 [ 2.          2.23606798  2.44948974]]


"""

print("standard deviation of the array is ",np.std(a),"\n"   )          # 1.490711985)

lists = []
j = np.hstack(a)
print(j,"hstack")

for i in j:
    x = (mean - i)**2
    lists.append(x)


print(lists)

list_sum = 0

for i in lists:
    list_sum = list_sum + i
print("The list sum is --",list_sum,type(list_sum),np.sum(list_sum))

#print "And the deviation is " (float(list_sum) / 9)






"""
    standard deviation is -->
    
    
    1.)    find the mean --->  (sum of all the values in the array)/no.of values = 2.66666666667
    2.)    differece of square for every element of x -->    
                 (2.66666666667-1)**2 = 2.777777778,(2.66666666667-2)**2 = 0.444444445,(2.66666666667-3)**2 = 0.111111111, 
                 (2.66666666667-2)**2 = 1.768,(2.66666666667 -3)**2 = 0.108,(2.66666666667 - 4)**2 = 0.4489, 
                 ( 2.66666666667 -4)**2 = 0.4489,(2.66666666667 -3)**2 = 0.108,(2.66666666667 - 2)**2 = 1.768
                 
    3.)           5.42 + 1.768 + 0.108 + 1.768 + 0.108 + 0.4489 + 0.4489 + 0.108 + 1.768 = 11.9458
    4.)            11.9458 / 9    = ~1.4
    

"""