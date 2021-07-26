member_adviser_email_ids = ''
mem_email_address = 'pavan@email.com'
addv_email_address = '' #None #'kumar@email.com'

if mem_email_address:
    member_adviser_email_ids = member_adviser_email_ids + mem_email_address + ';'
if addv_email_address:
    member_adviser_email_ids = member_adviser_email_ids + addv_email_address + ';'

print(member_adviser_email_ids)
