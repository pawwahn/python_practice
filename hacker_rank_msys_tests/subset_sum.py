

# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):
    # write your code in Python 3.6
    # pass
    from itertools import combinations
    d = {}
    k = set()
    for n in A:
        r = sum([int(i) for i in list(str(n))])
        k.add(r)
        d[n] = r
    d1 = {}
    for i in k:
        s = []
        for j in d.keys():
            if d[j] == i:
                s.append(j)
        if len(s) > 1:
            d1[i] = s
    if len(d1) >= 1:
        sum_list = []
        for i in d1.keys():
            for j in combinations(d1[i], 2):
                sum_list.append(sum(j))
        order_values = sorted(sum_list)
        return order_values[-1]
    else:
        return -1


li = [51, 17, 71, 42]

li1 = [42, 33, 60]

li2 = [51, 32, 43]

aa = solution(li1)
print(aa)       # ans:93




