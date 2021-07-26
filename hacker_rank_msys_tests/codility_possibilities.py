from itertools import permutations


A = ["abc", "kkk", "def", "csv"]
list_possibilities = []
list_result = []

for i in range(1, len(A) + 1):
    for j in permutations(A, i):
        list_possibilities.append(j)

#print(list_possibilities)

# print(list_result)

for i in list_possibilities:
    count_flag = False
    chars = "".join(i)
    for char in chars:
        count = chars.count(char)
        if count > 1:
            count_flag = True

    if not count_flag:
        list_result.append(len(chars))
print(max(list_result))
