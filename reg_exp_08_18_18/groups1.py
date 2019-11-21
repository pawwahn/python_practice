import re
a = 'user_name@hackerrank.com,pavanskt@gmail.com,' \
    'chaitu@gmail.com,kumar@gmail.com,kota.skt@gmail.com'
list_a=a.split(',')
group_list = []
for i in list_a:
    grp = re.match('(\w.+)@(\w+).(\w+)',i)
    if grp:
        group_list.append(grp.groups()) #try group(0) and group(1) and group(2) and group(3) and group()
print(group_list)






