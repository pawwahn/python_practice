import array as arr

my_array = arr.array('i',[1,2,3,4])     # should be 'i' but not any other value
print(my_array)
for i in my_array:
    print(i)
print(id(my_array))
print(id(my_array[0]))
print(id(my_array[1]))
print(id(my_array[2]))

print("************")
lst = [10, 20, '30', 20]
print(lst)
print(id(lst))
print(id(lst[0]))
print(id(lst[1]))
print(id(lst[2]))


#####c