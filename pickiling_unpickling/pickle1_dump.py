import pickle

a = ['a', 'b', 'c', 'd']

with open('text1.txt','wb') as file:
    pickle.dump(a,file)
file.close()

a = open("text1.txt",'rb')
pnt = pickle.load(a)
print(pnt)

