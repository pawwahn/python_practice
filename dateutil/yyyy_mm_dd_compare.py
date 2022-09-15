import time
# date1 = "31/12/2015"
# date2 = "01/01/2016"

date1 = "2015-12-31"
date2 = "2016-01-01"dic


newdate1 = time.strptime(date1, "%Y-%m-%d")
newdate2 = time.strptime(date2, "%Y-%m-%d")

if newdate1 >= newdate2:
    print("True")
else:
    print("False")