import os
print(os.getcwd())
try:
    f = open("dummy.txt")
except Exception as e:
    print(e)
    print("File not found")
    print ("continuing")
else:
    print ("else of file not found")
finally:
    print ("always exceutes finally")
