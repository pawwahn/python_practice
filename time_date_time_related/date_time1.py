
from dateutil import parser

input_date_str1 = 'Sun 4 May 2015 13:54:36 -0600'   #str(input())
input_date_str2 = 'Sun 4 May 2015 13:54:36 -0000'   #str(input())

t1 = parser.parse(input_date_str1)
t2 = parser.parse(input_date_str2)

print(int((t1-t2).total_seconds()))



