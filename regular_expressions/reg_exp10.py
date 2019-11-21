##  \d - matches any number in the given string 

import re

randstr = "125345 1125f6"

new_str = "123 123 1234 123 12345 123456 12345678 45678"

print randstr
print (re.findall("\d",randstr))                # ['1', '2', '5', '3', '4', '5', '1', '1', '2', '5', '6']

print (re.findall("\D",randstr))                 # ['', 'f']    --> non-digits

print ("matches", len(re.findall("\d",randstr) ))       # ('matches', 11)

print ("matches", len(re.findall("\D",randstr) ))       # ('matches', 2)

print "check",re.findall("\d[5]",randstr)               #    check ['25', '45', '25']

print "check length",re.findall("\d{2,3}",randstr)      #    check length ['125', '345', '112']

print ("matches" ,  len(re.findall("\d[5]", randstr) ) )

print ("matches",    len( re.findall("\d{5,7}",new_str)   ) )  # finds strings with the size {5,7} - meaning --> ['12345', '123456', '1234567', '45678']

print "check this conditions",re.findall('\d{5,7}',new_str)     #         ['12345', '123456', '1234567', '45678']
