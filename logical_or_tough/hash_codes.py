# 6
# Sample Output
#
#      #
#     ##
#    ###
#   ####
#  #####
# ######
# Explanation
#
# The staircase is right-aligned, composed of # symbols and spaces, and has a height and width of .

#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the staircase function below.
def staircase(n):
    a = " "
    #n = 6
    for i in range(1,n+1):#print(i)
        print(((n-i)*a)+("#")*i)
        #n=n-1

staircase(6)