a = [1,2,3,4,5,'a']
b = [10,20,30,40,50,'pavan']

cnt = 0
dic = {}
for i in a:
    dic[i] = b[cnt]
    cnt+=1
print(dic)

print(dic.items())
print(dic.keys())
print(dic.values())
print(dic.get('a'))
print(dic.__contains__('a'))