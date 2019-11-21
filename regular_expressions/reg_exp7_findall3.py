# use of ^(carat) symbol  -- ^ sym is for excpet that range but gives you rest

import re

str = "rat,pat,zat,fat,Mat,eat,Lat,zaq,cat,string,integer,mat,Zat"

allstr = re.findall('[M-s]at',str)        # show all paterns that matches with [M to s]= M-Z and a-s      ## output -- rat pat fat Mat eat cat mat Zat 
#allstr = re.findall('[^M-e]at',str)        # show all paterns that matches with everything except [M to e]      ## output -- rat pat zat fat Lat


for i in allstr:
    print(i)