import re

strng = "qwerty qw53tw eje934i dsfhosdf04fds spgks9sdf sdfsfsdr 234454g 453 "
email_strs = "qwhsa@sud.csdo aidj3z#sdf@hdm.cen pavan.sk@hmsi.co adj$sd@sk@.com qwlew23@ksd.co.ci 10e.197.75.251"

new_lst = re.findall('[a-z][0-9]',strng)
print(new_lst)

valid_emails = re.findall('[\w._]+@[\w._]+',email_strs)
print(valid_emails)

valid_ips = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',email_strs)
print(valid_ips)