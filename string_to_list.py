# str = '12345'
# x= list(str)
# print(x)
#
# lst = [1,2,3,4]
# y = str(lst)    ##str obj is not callable
# print(y)       ##str obj is not callable



#
#question
address = "address line 1 \r\n address line 2 \r\n address line 3"
#ans
add_list = address.split('\r\n')





print((add_list))
print(len(add_list))
add_count = add_list.__len__()
print (add_count)