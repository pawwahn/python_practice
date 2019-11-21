a = [1,2,3]
b = [4,5,6]
dic = {}
j = 0
for i in zip(a,b):
    dic[i[0]] = i[1]
print(dic)

#Dict Comprehension
item = {n: n*2 for n in range(5)}
print (item)

