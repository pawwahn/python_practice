import re

# \w means [a-zA-Z0-9_]   
# \W means [^a-zA-Z0-9_]         not what are present in the []

numbers = ['123-45a-7890', '231-125-5548','1294-98-554-','123-280-9989','789-987-7899','12a-222-2s11']
count = 0
for i in numbers:
    #if re.search("\w{3}-\w{3}-\w{4}",i):                       '''  we can use \w or \d -->> output will be same but here it checks for \w -- > [a-zA-Z0-9_]'''
    if re.search("\w{3}-\d{3}-\w{4}",i):                        #  we can use \w or \d -->> output will be same but here it checks for \d -- > [0-9]'''   
        print i
        count+=1
print "Total valid contact numbers are",count