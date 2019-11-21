# Two non-negative integers N and M are said to be similar  if their decimal representations can be obtained from each other by rearranging their digits. Note that a correct decimal representation does not contain leading zeroes (except for number 0).
# For example:
# that, given a non-negative integer N, returns the number of non-negative integers similar to N.

#1234 is similar to 2431
#1010 is similar to 1001
#123 is not similar to 234
#113 is not similar to 133
#100 is not similar to 10 (010 contains a leading zero)

#For example, given
# N = 1213 the function should return 12
# because there are twelve integers similar to 1213,
# namely: 1123, 1132, 1213, 1231, 1312, 1321, 2113, 2131, 2311, 3112, 3121 and 3211.


from itertools import permutations
num = 0
lst_num = str(num)
print(lst_num)
valid_combinations_count = 0
valid_combos = []
if num>0:
    for item in permutations(lst_num):
        if item[0] !='0' and item not in valid_combos:
            valid_combos.append(item)
            valid_combinations_count = valid_combinations_count+1
            #print (item)
    print(valid_combinations_count)