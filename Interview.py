import glob
path = r'C:\Users\56007\PycharmProjects\python_practice\regular_expressions'
#print(path)

member_num = '56007'
files = glob.glob1(path, 'FGTIP Sale Notice_'+member_num+'_*' +'.txt')
lst_files = []
for i in files:
    #print(i)
    lst_files.append((i.split('_')[5].split('.txt')[0]))

max_file_num = max(lst_files)
#print(max_file_num)
file_path = ''
for i in files:
    if max_file_num in i:
        file_path = path+'\\'+i
print(file_path)
    