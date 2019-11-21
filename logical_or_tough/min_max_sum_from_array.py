arr = [10,20,30,40,50]
# For example, . Our minimum sum is [1+2+3+4] and our maximum sum is [2+3+4+5]. We would print
#
# 16 24

size = len(arr)

sorted_list = sorted(arr)
min_sum,max_sum = 0,0
for i in range(size):
    if i>0:
        max_sum = max_sum + sorted_list[i]
    if i<size-1:
        min_sum = min_sum + sorted_list[i]
print(min_sum,max_sum)

