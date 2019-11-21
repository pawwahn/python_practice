# replace new line and print all the string in the same line
import re                                           ##   \b - backspace, \f - formfeed, \r - carriage return , \t - tab, \v - vertical tab
str = '''please print 
the double
slash         in 
the statement 
below
'''  
print str

regxp = re.compile("[\n]")

reg = regxp.sub(" ",str)

print reg
  
