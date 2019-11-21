import os
k = os.getcwd()
print k

if k == '/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/':
    os.mkdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/Matplot')
    fo =os.open('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/Matplot/matplot1.py','w+')
else:
    os.chdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/')
    os.mkdir('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/Matplot')
    fo =open('/home/likewise-open/HTCINDIA/pavankumark/Desktop/workspace/python_project/Matplot/matplot1.py','w+')