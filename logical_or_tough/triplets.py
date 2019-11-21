# Sample Input 0
# 5 6 7
# 3 6 10
# Sample Output 0
# 1 1
# Explanation 0
#
# In this example:
#
# Now, let's compare each individual score:
#
# , so Alice receives  point.
# , so nobody receives a point.
# , so Bob receives  point.
# Alice's comparison score is , and Bob's comparison score is . Thus, we return the array .
#
# Sample Input 1
#
# 17 28 30
# 99 16 8
# Sample Output 1
#
# 2 1



def triplets(a,b):
    a_sum = 0
    b_sum = 0
    for i,j in a,b:
        print(a[i])
    #     if a[i] > b[j]:
    #         a_sum = a_sum+1
    #     elif a[i] < b[j]:
    #         b_sum = b_sum+1
    #     else:
    #         pass
    # return (a_sum,b_sum)

print(triplets([1,2,3],[4,5,1]))














