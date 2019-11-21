lists = ['white','pink','Blue','Red']
clr = input('Enter the color you wish to find ??')
print(clr)
try:
    if clr in lists:
        print ("{} color found".format(clr))
    else:
        print("Color not found ")
except Exception as e:
    print (e)
    print ("IOException: Color not found")
finally:
    print("There are several colors in the world")

