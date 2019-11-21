num = 8
bin_num = ""
while(num>=1):
    if (num%2==0):
        bin_num = bin_num+"0"
        num = num/2
    else:
        bin_num = bin_num + "1"
        num = (num - 1)/2
len_bin = len(bin_num)
binary_number = ""
while(len_bin>0):
    binary_number = binary_number + bin_num[len_bin-1]
    len_bin-=1
print(binary_number)











