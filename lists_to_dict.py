a = [1,2,3,4,5,'a']
b = [10,20,30,40,50,'hex']

cnt = 0
dic = {}
for i in a:
    dic[i] = b[cnt]
    cnt+=1
print(dic)

# print(dic.items())
# print(dic.keys())
# print(dic.values())
# print(dic.get('a'))
# print(dic.__contains__('a'))

a = [1,2,3,4,5]
b = [10,20,30,40,50]
# res = {}
# for key in a:
#     for value in b:
#         res[key] = value
#         b.remove(value)
#         break
# print(str(res))

res = {a[i]: b[i] for i in range(len(a))}
print(str(res))