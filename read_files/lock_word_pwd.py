import pyminizip
import win32com.client

# input file path
inpt = "D:\\LV\\LiverPool_Design.docx"

# prefix path
pre = None

# output zip file path
oupt = "D:\LV\LiverPool_Design.zip"

# set password value
password = "Password123"

# compress level
com_lvl = 5

# compressing file
pyminizip.compress(inpt, None, oupt,
                   password, com_lvl)