# Sample Input
#
# 6
# -4 3 -9 0 4 1
# Sample Output
#
# 0.500000
# 0.333333
# 0.166667
# Explanation
#
# There are 3 positive numbers, 2 negative numbers, and 1 zero in the array.
# The proportions of occurrence are positive:3/6=0.500 , negative:2/6=0.33
# and zeros: 1/6=0.167

# Complete the plusMinus function below.
def plusMinus(arr):
    arr_length = len(arr)
    positive_elements_count = 0
    negative_elements_count = 0
    zeros_count = 0
    print("arr_length is {}".format(arr_length))
    for i in range(arr_length):

        if arr[i]>0:
            #print("------------>>>>",arr[i])
            positive_elements_count =  positive_elements_count+1
        if arr[i] < 0:
            #print("------------<<<<<<<", arr[i])
            negative_elements_count = negative_elements_count+1
        if arr[i] ==0:
            #print("------------00000000", arr[i])
            zeros_count = zeros_count+1
    positive = positive_elements_count / arr_length
    negative = negative_elements_count / arr_length
    zero = zeros_count / arr_length
    print("positive --",positive)
    print("negative --",negative)
    print("zeros ",zero)

if __name__ == '__main__':
    #n = int(input())

    arr = list(map(int, input().rstrip().split()))

    plusMinus([-1,0,2,-1,-4])
