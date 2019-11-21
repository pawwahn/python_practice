# match series of range of characters
import re

#str = "rat,pat,zat,Fat,mat,zaq,cat,string,integer"
str = "rat,pat,zat,fat,Mat,zaq,cat,string,integer hat Hat"

allstr = re.findall('[F-P]at',str)           #  search all characters from F to P -- not small [f-p]

for i in allstr:
    print i