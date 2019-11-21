thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

for i in thisdict:
    print("key and values are: {} ---> {}".format(i,thisdict[i]))
print("-----\n")
for i in thisdict.keys():
    print(i)
print("++++ dict values +++++\n")
for i in thisdict.values():
    print(i)

print("*****for dict items below*****\n")
for i,j in thisdict.items():
    print(i,j)

print("check key availbale in the dict or not")
if 'brand' in thisdict:
    print("Key is present")
else:
    print("Key is not present")

print("The length of dict is :{}".format(len(thisdict)))

print("lets add new key value to the dict below")
thisdict['version']=2.0
print("updated dict is {}".format(thisdict))

print("remove a key from the dict below")

thisdict.pop('brand')
print("updated dict is {}".format(thisdict))