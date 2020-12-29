from datetime import datetime
import pytz

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')

EST = pytz.timezone('US/Eastern')

# print the date and time in
# standard format
print("UTC in Default Format : ",
	datetime.now(UTC))

print("IST in Default Format : ",
	datetime.now(IST))

# print the date and time in
# specified format
datetime_utc = datetime.now(UTC)
print("Date & Time in UTC : ",
	datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z'))

datetime_ist = datetime.now(IST)
print("Date & Time in IST : ",
	datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))


datetime_ist = datetime.now(EST)
print("Date & Time in EST : ",
	datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
