dic = {'a':1,'b':2,'c':3}

for k,v in dic.items():
    print(k,v)

print(dic.keys())
print(dic.values())
print(dic.items())
new_dic = dic.copy()
print("new_dic values are: {}".format(new_dic))

#removes the key 'b' and its value
dic.pop('b')
print(dic)      #{'a': 1, 'c': 3}

print(dic.fromkeys('a'))
# print(dic.clear())
# print(dic)

l1 = [1,2,3]
l2 = [10,20,30]
d1 = zip(l1,l2)
print(set(d1))

