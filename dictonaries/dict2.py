thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
    'version': 2.0,
    'purchased on':2019
}

print(thisdict)
print("pop a key from the dict below")
thisdict.pop('brand')
print("updated dict is {}".format(thisdict))

print("-----popitem below")

thisdict.popitem()
print("updated dict is {}".format(thisdict))

print("----del below")
del thisdict['year']
print("updated dict is {}".format(thisdict))

print("clear all the dictonary ")
thisdict.clear()
print("updated dict is {}".format(thisdict))
