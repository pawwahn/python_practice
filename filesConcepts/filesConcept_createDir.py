import os
k = os.getcwd()
if k == '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project':
    os.makedirs('numpy concepts')
    print "directory created"
else :
    os.chdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project')
    os.makedirs('numpy concepts')
    print "directory created"