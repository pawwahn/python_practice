import os
file = open('text.txt','r')
data = "We are writing a data to th files"
file.write(data)
file.close()

print os.getcwd()