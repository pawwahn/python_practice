import re
s = 'blahblah@gmail.com'
domain = re.search("@[\w.]+", s)
print domain#.group()
