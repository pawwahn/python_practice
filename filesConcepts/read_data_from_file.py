import os
fr = open('text.txt','r')
data = fr.read()
#print "Data in the file is: \n",data
characters = len(data)
print ("Number of caharcters in the file are: ",characters)
lines = data.split('\n')
words = 0
print ("Number of lines in the data are: ",len(lines))
for line in lines:
    words+=len(line.split(' '))
print ("number of words:",words)