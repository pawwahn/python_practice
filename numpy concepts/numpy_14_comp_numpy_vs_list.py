import numpy as np
import time

start_time = time.time()
# a = np.arange(10000)
a = range(10000)
print a
k =[i+5 for i in a]
print k
end_time = time.time()

t1 = (end_time - start_time )*100

start_time = time.time()
a = np.array(a)
b = a+5
print b
end_time = time.time()
t2 = (end_time - start_time )*100

if t1 > t2:
    print "a is big",t1,t2,t2-t1
else:
    print "b is big",t1,t2,t2-t1