# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):
    # write your code in Python 3.6
    import copy
    m = []
    # n2=696
    m.append(A)
    r = [int(i) for i in list(str(A))]
    new_list = []

    for i in range(len(r)):
        t = copy.deepcopy(r)
        t[i] = (9 if r[i] == 6 else 6)
        new_list.append(t)
        t = []
    for i in new_list:
        s = int("".join([str(i) for i in i]))
        m.append(s)
    return max(m)

#a = solution(696)
a = solution(698)
a = solution(123)
print(a)