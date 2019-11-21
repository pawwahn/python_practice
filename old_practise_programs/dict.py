# for i in (1,2,3,4):
#     print i

dict = {'three':3,'one':1,'two':2,}
print (dict.keys())
print (dict.values())
new_dict = dict.copy()
print (new_dict)
dict['three'] = 03.2
print (dict)
print (new_dict)

#print (dict.has_key('one'))
print('one' in dict )
print (dict.__sizeof__())
print (dict.items())
a = [1,2,3]
b = ['a','b','c']
new_dc = zip(a,b)
#print(new_dc.__dict__)
print(set(new_dc))