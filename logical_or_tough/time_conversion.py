t1 = '12:05:45AM'
#print(t1[0:-2])


def timeConversion(t1):
    partial_hr = int(t1[:2])
    other_time = (t1[2:-2])
    #print(partial_hr)
    check_am_pm = t1[-2:]
    if check_am_pm.upper() =='PM':
        if partial_hr<=12:
            new_time = partial_hr+12
            converted_time = str(new_time)+other_time
        return converted_time
    else:
        return t1[0:-2]

print(timeConversion(t1))