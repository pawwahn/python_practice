import os

#print(os.getcwd())
#obj = open('C:\\Users\pakota\Desktop\pytohn_practise\mnc_int_questions\dummy_filr','r')
obj = open('Y:\\Python_code_practise_2019\python_practise\mnc_int_questions\dummy_filr','r')
#print(obj)
file_obj= obj.read()

#length of data or num of characters in the file
data_len = len(file_obj)
print(data_len)

#no of lines
no_of_lines = file_obj.split("\n")
print(len(no_of_lines))

# no of words
no_of_lines = file_obj.split(" ")
print(len(no_of_lines))