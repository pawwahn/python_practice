# replace a word in the given string
# to replace a word or substring , we need to compile by giving the search pattern 
import re
str = "rat pat 'zat' 'fat', 'Mat' ,'hat' ,'Lat', zaq cat string integer"

#regx = re.compile("[d-z]at")                  # output --- food food food food Mat food  Lat  zaq  cat  string integer

out_put1 = re.findall("[^d-z]at",str)
print "output 1*--->",out_put1

regx = re.compile("[^d-z]at")                  # output --- rat   pat  zat  fat food hat food  zaq  food string integer    ## used ^ sym
#print regx,"\n"

str1 = regx.sub("food",str)

print str1,"\n"

out_put2 = re.findall("[d-z]at",str)
print "output 2*--->",out_put2


regx1 = re.compile("[d-z]at")
print regx1,"\n ------------>>"
str2 = regx1.sub("dude",str)                    # dude dude 'dude' 'dude', 'Mat' ,'dude' ,'Lat', zaq cat string integer
print str2                          