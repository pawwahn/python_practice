import re
nameAge = '''
John is 11 and Theon is 12
Kota is 24 and Pavan is 24
'''

# {'john':11,'Theon':12}

ages = re.findall(r'\d{1,2}',nameAge)
names = re.findall(r'[A-Z]{1}[a-z]{1,10}',nameAge)
print (ages)
#print names
# i = 0
# dict = {}
# for name in names:
#     dict[name] = ages[i]
#     i+=1
# print dict