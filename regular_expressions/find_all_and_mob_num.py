import re

str = """Regular expressions can be concatenated to9000016054form new regular expressions; if A and B are both regular expressions, then AB is also a regular expression. In general, if a string p matches A and another string q matches B, the string pq will match AB. This holds unless A or B contain low precedence operations; boundary conditions between A and B; or have numbered group references. Thus, complex expressions can easily be constructed from simpler primitive expressions like the ones described here. For details of the theory and implementation of regular expressions, consult the Friedl book referenced above, or almost any textbook about compiler construction.
A brief exp9884445699lanation of the format of regular expressions9884445938 follows.For further information and a gentler presentation, consult the Regular Expression HOWTO.
pavan.skt@gmail.co.inRegular expressions can 2*989895869 contain evn both special and ordinary 985*558541 characters. Most ordinary characters, like 'A', 'a', or '0', are the simplest regular expressions; they simply match themselves. You can concatenate ordinary characters, so last matches the string 'last'. (In the rest of this section, we’ll write RE’s in this special style, usually without quotes, and strings to be matched 'in single quotes'.)
Some characters,likezdz'|'pation wapationcterzation pavan ravan qansm qavan *ano pavan.skt@gmail.com pa@van.skt@gmail.compavan.skt@gma@il.comorer rr pavankumar '(', are special. Sp985447526ecial 94e584d415 characters either 99874587412stand for classes of ordinary characters, or affect how the regular expressions around them are inter
John is 11 and Theon is 12
Kota is 24 and Pavan is 24
"""

import re

num = re.findall("[0-9]{10}",str) # this is for extracting phone numbers
print(num)

five_letters = re.findall("\w{5}",str)   # this is to make whole string in to 5 letter word partition
#print(five_letters)

five_num = re.findall("\d{5}",str)   # this is to make whole string in to 5 letter word partition
print(five_num)

between_letter = re.findall("p\w{2,4}l",str)
#  this gives results of words starts $ ends with 'p and l' where the between letters size will be 2-4
#print(between_letter)

ava = re.findall("\wava\w",str)
#  this gives results of words that contains 'ava' in the string
#print(ava)

allstr = re.findall('[pzif]a[\w]{2,4}',str)
# should start with r|p|z|i|m|f 'a' and anyword of size{2-4}
#print(allstr)

allstr = re.findall('[p-r]a[\w]{3}',str)
# should start with r|p|z|i|m|f 'a' and anyword of size{3}
#print(allstr)

allstr = re.findall('[pr]a[\w]{2}',str)
# should start with r|p 'a' and anyword of size{2}
print(allstr)

allstr = re.findall('\Wa\w{2,3}',str)
# should start with non-alphanumeric 'a' and anyword of size{2-3}
print(allstr)

emails = re.findall("[\w._]{6,}@[\w]{2,5}.[com,co.in]{2,5}",str)
print(emails)

name_age_list = re.findall("[A-Z]{1}[a-z]{2,} is \d{1,2}",str)
print(name_age_list)

dic = {}
x = 0
for i in name_age_list:
    name = re.findall("[A-Z][a-z]*",i)
    age = re.findall("\d{2}",i)
    dic[name[0]] = age[0]
print(dic)
