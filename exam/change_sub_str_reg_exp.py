import re
str = 'this is just writen as i do not know what to write in a string'
rep = re.compile(r'i')

replace = rep.sub('I',str)
print (replace)
str.replace('a','A')
print(str)
print(str.replace('a','A'))
print (str.isupper())
print (str)
print (str.count('a'))