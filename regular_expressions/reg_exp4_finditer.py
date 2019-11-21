# use of finditer()

# finditer() gives the position of the search word

import re
str = "count num of words in the word inform and inform to the team regarding the 'inform' word count information"
tup = ()
lst =[]

# k = re.findall('inform',str)
# print k

for i in re.finditer('inform', str):
     print (i)
     print (i.span())                 # gives the start and end position of each search word
     #print (lst)                      # gives indiv position of search word
#      lst.append(tup)  
# print (lst)
            