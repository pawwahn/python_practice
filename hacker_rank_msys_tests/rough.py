# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

from itertools import permutations

list_possibilities = []
list_result = []

def other_solution(A):

    return list_possibilities

def solution(A):
    # write your code in Python 3.6
    for i in range(1, len(A) + 1):
        for j in permutations(A, i):
            list_possibilities.append(j)

    #print("-------------",list_possibilities)
    for i in list_possibilities:
        count_flag = False
        chars = "".join(i)
        for char in chars:
            count = chars.count(char)
            if count > 1:
                count_flag = True

        if not count_flag:
            list_result.append(len(chars))

    if list_result:
        return (max(list_result))
    else:
        return 0



A = ['potato', 'kayak', 'banana', 'racecar']
aaa = solution(A)
print(aaa)