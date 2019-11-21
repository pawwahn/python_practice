# Sample Input
#
# 3
# 11 2 4
# 4 5 6
# 10 8 -12
# Sample Output
#
# 15
# Explanation
#
# The primary diagonal is:
#
# 11
#    5
#      -12
# Sum across the primary diagonal: 11 + 5 - 12 = 4
#
# The secondary diagonal is:
#
#      4
#    5
# 10
# Sum across the secondary diagonal: 4 + 5 + 10 = 19
# Difference: |4 - 19| = 15






a = [[11,2,4],
     [4,5,6],
     [10,8,-12]]

size = len(a)-1

#print(a)
j,k = 0,size
sum1,sum2 = 0,0
for x in a:
    print("x[k] value is {} ".format(x[j]))
    sum1 = (x[j]) + sum1        #11
    print("sum1---->>>{}".format(sum1))
    j+=1
print("left diagonal sum is {}".format(sum1))
print("****************************")
for y in a:
    print("y[k] value is {} ".format(y[k]))
    sum2 = (y[k]) + sum2
    print("sum2---->>>{}".format(sum2))
    k-=1

print("right diagonal sum is {}".format(sum2))
diff = (sum1)-(sum2)
#print(diff)
print(abs(diff))
