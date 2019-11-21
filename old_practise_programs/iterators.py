a = ('hello','Bro','How','are','you')

# for i in a:
#     print i

itr = iter(a)             # iter(obj) is a function which gives the o/p as tupleIterator and to view the o/p, we need to use next()
print itr                 #       <listiterator object at 0x00876A90>

print next(itr)
print next(itr)
print next(itr)
print next(itr)
print next(itr)
#print next(itr)

rev_itr = reversed(a)
print next(rev_itr)
