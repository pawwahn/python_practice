def remote_control():
    yield "Pavan"
    yield "Kota"
    yield "Kumar"

itr = remote_control()
print(itr)
print (next(itr))

print(itr)
print (next(itr))

print(itr)
print (next(itr))

#print (next(itr))