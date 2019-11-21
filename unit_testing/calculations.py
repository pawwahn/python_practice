
def squares(lst):
    sqr_lst = []
    for i in lst:
        sqr_lst.append(i*i)
    return sqr_lst

def cubes(lst):
    cube_lst = []
    for i in lst:
        cube_lst.append(i*i*i)
    return cube_lst

def add_num(lst):
    tot = 0
    for i in lst:
        tot+=i
    return tot

def div(x,y):
    if y==0:
        raise ValueError("can not divide with zero")
    return x/y

