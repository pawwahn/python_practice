import re
s1 = 'abc$$d$ef'
s2 = 'abc>>d$ef'

pattern1 = r'\$\$+'
pattern2 = r'>>+'

print(re.sub(pattern1, 'P', s1))
#for $ u have to use / before it, bcz $ is having an importance in regular exp


print(re.sub(pattern2, '^^', s2))

