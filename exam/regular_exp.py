import os
import re
files = open('mails.txt','r')
#files = open('mails2.txt','w+')
data = files.read()
emails = re.findall(r'[a-zA-Z0-9._]{5,20}@[a-zA-Z.]{2,10}',data)
print(emails)