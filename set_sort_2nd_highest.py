s = '1,6,2,4,1,5,2,6,7,1,4'
int_list = list(set([int(i) for i in s.split(',')]))
print(int_list[-2])