import pickle

a = {'name':'Pavan','age':27,'gender':'M'}

with open('dict.txt','wb') as file:
    pickle.dump(a, file)
file.close()