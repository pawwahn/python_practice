import pickle

a = open('dict.txt','rb')
b = pickle.load(a)
print(b)
print(type(b))
