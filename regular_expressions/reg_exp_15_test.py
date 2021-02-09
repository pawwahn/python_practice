# find valid contact numbers and valid emails and replace the mail id of anything with @htcindia.com

import re

numbers = ['123-445-9987','156-995-8744','988-985-954','q12-9as-44ss']
#mails = ['a@gmail.com','abc@xyz.com','kota@skt.com','pavan.kota@gmail.com','12pP@htc.com','3452.234@abc.com','a@b.co']
mails = 'a@gmail.com','abc@xyz.com','kota@skt.com','pavan.kota@gmail.com','12pP@htc.com','3452.234@abc.com','a@b.co'


valid_numbers = []
valid_mails = []
num_count = 0
mail_count = 0
new_str = ''

for i in numbers:
    if re.findall("\d{3}-\d{3}-\d{4}",i):
        num_count+=1
        valid_numbers.append(i)

print ("The count of valid numbers are",num_count,"and the valid numbers are ",valid_numbers)

for j in mails:
    if re.findall("[A-Za-z0-9+-_.]{2,20}@[A-Za-z]{2,6}[.A-Za-z]{2,4}",j):
        mail_count+=1
        valid_mails.append(j)

print ("The number of valid mail address are ",mail_count," and they are ",valid_mails)

# for ind in valid_mails:
#     new_string = str(ind)+", "
#     new_str += new_string
# print new_str
#
#
# reg_exp = re.compile("@[A-Za-z+-_.]{2,5}.com")
# m = reg_exp.sub("@htc.com",new_str)
# print m