import datetime
from datetime import datetime,timedelta

input_date_str = str(input())
no_of_days_add = input()

converted_input_date = datetime.strptime(input_date_str, '%d-%m-%Y')

new_datetime_format = '%a %d %b %Y %H:%M:%S %z'
# print(input_date_str)
# print(no_of_days_add)
print(converted_input_date)
# print(type(converted_input_date))

new_date = converted_input_date + timedelta(days=100)
print(new_date)







