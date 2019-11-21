""" 
This file is to check current directory and create a new file 'regular_concept2' in regular exp folder

"""
import os
k = os.getcwd()    # get current working directory
print k
if k == '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression':
    fo = open('regular_concept2.py','w+')
else:
    os.chdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression')  # chANGEdirECTORY
    fo = open('regular_concept2.py','w+')
    