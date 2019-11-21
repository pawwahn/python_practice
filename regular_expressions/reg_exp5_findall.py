import re

str = "rat,pat,zat fat,mat,zaq,1at,cat,string,integer"

allstr = re.findall('[rpzimf]a[\w]{1}',str)         # rat pat zat fat mat zaq
#allstr = re.findall('.at',str)
#allstr = re.findall('[rpzimf]at',str)               # rat pat zat fat mat
#allstr = re.findall('[Rpzimf]at',str)             # no rat -- case sensitive

#allstr = re.findall('[^Rpzim]at',str)               # rat fat lat cat

for i in allstr:
    print(i)