orderDict = {'PhoneNumber':1, 'SMSPhoneNumber':2, 'EmailAddress':3, 'Address':4}

res = []

for key in orderDict.keys():
    res = orderDict[key]
    print(res)
#print(sorted(list(res)))

