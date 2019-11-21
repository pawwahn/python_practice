# email validations
import re

emails = ['a@s.c', 'kota@gmail.com', 'pavan.kota@yah.com', 'abc@xyz.com']
count = 0
valid_emails = []
for i in emails:
    if re.search("[\w.+-_]{3,20}@.[A-Za-z]{2,3}",i):
        count += 1
        valid_emails.append(i)
        
print(valid_emails)
print(count)  