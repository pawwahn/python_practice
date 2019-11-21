import re

x = "guru99, god gun gender education,+ is fun"

z = re.match("(g\w+)\W+(\w+)",x)
#print(z)

###

sentence = 'we are humans'
matched = re.match(r'(.*) (.*?) (.*)', sentence)
print(matched.groups())

sentence = '~we2 are@ humans-'
matched = re.match(r'(.*) (.*) (.*)', sentence)
print(matched.groups())

sentence = '~we2 %^$ are@ humans- %$B#%B hats #@#$ $@ DE33'
matched = re.match(r'(.*) (.*) (.*)', sentence)
print(matched.groups(4))