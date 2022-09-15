# Python3 program to find number of days
# between two given dates
from datetime import date


def numOfDays(date1, date2):
    return (date2 - date1).days

cur_date = date.today()
#print(cur_date)

yy,mm,dd = cur_date.year, cur_date.month, cur_date.day
#print(yy,mm,dd)

# Driver program
date1 = date(1947, 12, 13)
date2 = date(yy, mm, dd)
print(numOfDays(date1, date2), "days")


