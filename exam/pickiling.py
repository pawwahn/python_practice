#
import pickle

file = open('test.txt','wb')
obj_1 = ['test_1', {'ability', 'mobility'}]
pickle.dump(obj_1, file)
file.close()
print("-------")
file = open('test.txt', 'rb')
pobj_1 = pickle.load(file)
#print(dir(pickle))
print(pobj_1)

file.close()