""" 
This file is to check current directory and create a new file 'regular_concept2' in regular exp folder

"""


import os
cur_work_dir = os.getcwd()
print (cur_work_dir)
if cur_work_dir == '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression':
    fo = os.rename('regular_exp.py', 'regular_exp1.py')
else:
    os.chdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression')
    fo = os.rename('regular_exp.py', 'regular_exp1.py')


