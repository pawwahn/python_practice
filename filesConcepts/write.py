fh = open("dummy1.txt",'a')
lines = ["line 1 \n","line2 \n","line3 \n"]
fh.writelines(lines)
take_input = raw_input("enter data")
fh.write(take_input)
fh.close()

fh = open("dummy1.txt",'r')
print fh.read()
fh.close()