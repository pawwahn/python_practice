import os
try:

    fh = open('dump.txt','w+')
    print ("11111111111")
    data = input("Enter string to write in the file")
    fh.writelines(data)
except IOError as i:
    print(i)
else:
    print ("data written in th string and the data is as follows: {}".format(fh.read()))
    print (fh.read())

    fh.close()
# try:
#     fb = open('dump.txt','r')
#     print "222222222"
#     print fb.mode
#     if fb.mode == 'r':
#         fb = open('dump.txt','w')
#         fb.write("new line added")
#         fb_obj = fb.readlines()
#         print fb_obj
# except IOError as i:
#
#     print i
