str ="Pavan Kumar"
new_rev_str = ""
len_of_str = len(str)-1
print(len_of_str)
while(len_of_str>=0):
    new_rev_str = new_rev_str+str[len_of_str]
    len_of_str-=1
print(new_rev_str)