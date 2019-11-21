
import re
nameAge = '''
John is 11 and Theon is 12
Kota is 24 and Pavan is 24
'''
                                                       # findall() for list of all matches in the string
ages = re.findall(r'\d{1,3}', nameAge)                 #d{1,3}  ---> d for digits and {1,3} size of the digits should be between 1 and 3
names = re.findall(r'[A-Z][a-z]*',nameAge)             # [A-Z] --> 1st letter should be capital and [a-z] is next letter should be small and * for n number of alphabets of small 

#print ages
#print names
ageDict = {}
x = 0

for eachname in names:
    ageDict[eachname] = ages[x]
    x+=1
print (ageDict)

nameDict = {}
y = 0
for age in ages:
    nameDict[age] = names[y]
    y+=1
print(nameDict)
