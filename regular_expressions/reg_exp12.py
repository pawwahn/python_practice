# name validation

import re
names = ['Kota1 pavan','kota pa12van','KOta Pa1','KOta pa1','Pa1 KK',
         'kp kumar','k k c','kk chaitanya']
count =0
valid_name_list = []
for i in names:
    if re.search("[A-Za-z]{2,20}[0-9]\s\w{2,20}",i):
        count += 1
        valid_name_list.append(i)
        
print count
print valid_name_list



'''
1.  \w{2,20}\s\w{2,20}   ---------- > \w{1st name should be word of size 2-20}\s- {\n,\t,\v,\f - any space characters}\w{last name should be word of size 2-20}

2.  [A-Za-z]{2,20}[0-9]\s\w{2,20} --> [1st name should be of A-Za-z of size 2-20][0-9 -> after words next should be number from 0-9]\s- {\n,\t,\v,\f - any space characters}\w{last name should be word of size 2-20}

3. 


to remember : \s- [\n\t\v\f] \S - [^\n\f\n\t]
'''