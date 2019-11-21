import numpy as np
a = np.array([ (1,2,3,4),(5,6,7,8),(9,10,11,12)   ])
#print a,a.size
a = a.reshape(4,3)
print a,"\n"
#print a[3,2]
print a[0:2],"\n 11111 \n"
print a[0:3],"\n 2222 \n"
print a[0:4,1],"\n 33333 \n"                  # [ 2  5  8 11]

print a[0:3,1],"\n 44444 \n"                  #  [2 5 8]  
print a[1:3,1] ,"\n 555555 \n"                 #   [5 8]

print a[2:3,0],"\n 66666 \n"                  #   [7]