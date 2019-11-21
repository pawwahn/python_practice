import re

str = """wReg@ular expressions can be concatenated to 9000016054 form new regular expressions; if A and B are both regular expressions, then AB is also a regular expression. In general, if a string p matches A and another string q matches B, the string pq will match AB. This holds unless A or B contain low precedence operations; boundary conditions between A and B; or have numbered group references. Thus, complex expressions can easily be constructed from simpler primitive expressions like the ones described here. For details of the theory and implementation of regular expressions, consult the Friedl book referenced above, or almost any textbook about compiler construction.
A brief exp9884445699lanation of the format of regular expressions 9884445938 follows. For further information and a gentler presentation, consult the Regular Expression HOWTO.pavan.skt@gmail.co.inRegular expressions can 2*989895869 contain evn both special and ordinary 985*558541 characters. Most ordinary characters, like 'A', 'a', or '0', are the simplest regular expressions; they simply match themselves. You can concatenate ordinary characters, so last matches the string 'last'. (In the rest of this section, we’ll write RE’s in this special style, usually without quotes, and strings to be matched 'in single quotes'.)
Some characters, likezdz '|' pation wapationcterzation pavan ravan qansm qavan *ano pavan.skt@gmail.com pa@van.skt@gmail.compavan.skt@gma@il.comorer rr pavankumar '(', are special. Sp985447526ecial 94e584d415 characters either 99874587412stand for classes of ordinary characters, or affect how the regular expressions around them are inter"""


match = re.match("\w{4}[.@]",str)       # gives the 1st match
print(match)

