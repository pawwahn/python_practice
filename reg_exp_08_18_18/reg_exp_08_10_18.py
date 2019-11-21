#findall()

import re
x = "guru99,education,+ is fun"

r1 = re.findall(r"^\w",x)       #^\w - matches the start of the alphanumeric
print(r1)   #   ['g']

r1 = re.findall(r"\w",x)        # \w - splits all the alphanumeric values
print(r1)       #   ['g', 'u', 'r', 'u', '9', '9', 'e', 'd', 'u', 'c', 'a', 't', 'i', 'o', 'n', 'i', 's', 'f', 'u', 'n']

r1 = re.findall(r"\w+",x)       #   \w+ - splits all the words
print(r1)       #   ['guru99', 'education', 'is', 'fun']

r1 = re.findall(r"^\w+",x)      #   ^\w+ - gives the 1st word
print(r1)       #   ['guru99']

r1 = re.findall(r"^\W",x)       #   ^\W -   matches the 1st non-alphanumeric key
print(r1)   #   []

r1 = re.findall(r"\W+",x)       #   \W+ -   matches all the non-alphanumeric keys
print(r1)   #   [',', ' ', ' ']



