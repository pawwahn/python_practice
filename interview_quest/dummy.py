lst = [2,4,5,2,1,7,4,9,10]
length = len(lst)
valid_values = []
#print("The length of list is : {}".format(length))


def area_rect(biggest_value):
    area = biggest_value*1
    return area

for i in range(0,len(lst)):
    if i+1 < length:
        if lst[i]+1 == lst[i+1]:
            valid_values.append(lst[i]+lst[i])
        else:
            pass
    else:
        pass
big_value = max(valid_values)
highest_area = area_rect(big_value)
print("The highest area is : {}".format(highest_area))
