a = [3, 5, 6, 3, 3, 5]


res = 0
ls1 = []
ls2 =[]
inc = 0
for i in range(len(a)):
    for j in range(i+1,len(a)):
        ls1.append(i)
        ls2.append(j)
a = list(zip(ls1,ls2))
print(a)
