q = [x**2 for x in [1,2,3,4,5,6]]
print(q)

ls = ["    pavan    ","kumar    ","      kota"]

str_lst = [i.rstrip() for i in ls]  #strips only right
print(str_lst)

str_lst = [i.lstrip() for i in ls]  #strips only left
print(str_lst)