import re
x = "guru99,education is fun"
r1 = re.findall(r"\w",x)
print(r1)

r1 = re.findall(r"\w+",x)
print(r1)

r1 = re.findall(r"^\w+",x)
print(r1)
