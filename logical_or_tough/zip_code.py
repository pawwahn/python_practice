sms = "SMS messages are really short"
sms_length = len(sms)
#print(sms_length)
valid_sms_length = 12
new_list_size = int(sms_length / valid_sms_length) + (sms_length % valid_sms_length >0)
print(2 + (sms_length % valid_sms_length >0))
print(new_list_size)

