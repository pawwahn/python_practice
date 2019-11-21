a = [1,2,3]
b = [1,4,2]

a_sum,b_sum = 0,0

print(list(zip(a,b)))
for i in zip(a,b):
    if i[0] > i[1]:
        a_sum = a_sum+1
    elif i[0] < i[1]:
        b_sum = b_sum+1
    else:
        pass
new_list=[a_sum,b_sum]
print(new_list)
