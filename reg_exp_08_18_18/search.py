import re

lst = ['Event','Username','Endpoint Id','Source Timestamp']
new_lt = []
for i in lst:
    if re.match("[AEIOU][a-z]*",i):
        new_lt.append(i)
print(new_lt)



str = " 'Event','Username','Endpoint Id','Source Timestamp' "
new_lst = re.findall("[AEIOU][a-z]*",str)
print(new_lst)



#result is different -- bcz one is string and the other is list
