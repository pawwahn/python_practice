""" find a word in the pattern"""

import re

string1 = "let's inform the latest information for the team"

if re.search('inform', string1):                                    # search() for searching whether search pattern is present or not 
    print ("search pattern word is found in the given string")
else:
    print ("search pattern word is not found in the given string")

