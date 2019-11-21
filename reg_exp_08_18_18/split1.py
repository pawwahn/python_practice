import re
a = '100,000,000.00'

ls = re.split('[.,]',a)
print(ls)