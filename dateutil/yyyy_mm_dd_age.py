from datetime import datetime
from datetime import date
from dateutil import relativedelta


mem_dob = '27-05-1964'.split('-') #working date #27-05-1925, 04-05-1947,
#mem_dob = '04-05-1952'.split('-')

mem_dob_date = datetime(int(mem_dob[2]), int(mem_dob[1]), int(mem_dob[0]))
current_date = date.today()

yy,mm,dd = current_date.year, current_date.month, current_date.day
current_date = date(yy, mm, dd)

diff = relativedelta.relativedelta(current_date, mem_dob_date)

years,months,days = diff.years, diff.months, diff.days

print('{} years {} months {} days'.format(years, months, days))
# 7 years 10 months 17 days

#if ((years >=74 and months >=11) or (years >= 75 and months==0) or  (years >= 75 and months < 2)):
if ((years ==74 and months >=11) or (years == 75 and months==0) or  (years == 75 and months < 2)):
    print("Member is close to 75th birthday")
else:
    print("Not close to 75")