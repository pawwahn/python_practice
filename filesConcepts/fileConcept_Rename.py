#renaming a file

import os

if os.getcwd() == '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression':
    fo = os.rename('regular_concept2.py', 'reg_exp2.py')
    print("file is renamed")
else:
    os.chdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/regular expression')
    fo = os.rename('regular_concept2.py', 'reg_exp2.py')
    print ("file is renamed")
