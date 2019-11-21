from matplotlib import pyplot as plt
import numpy as np

x = np.arange(0,5,0.1)
#print x
y = np.cos(x)
#print y
#plt.plot(x,y)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
#plt.subplot(211)

x1 = np.arange(0,8,0.2)
#print x1
y1 = np.sin(x1)

x2 = np.arange(0,4,0.3)
#print x1
y2 = np.sinh(x2)

#print y1
#plt.plot(x1,y1)
# plt.plot(x,y)
# plt.plot(x1,y1)
# plt.plot(x2,y2)

plt.plot(x,y,'bo',x1,y1,'bo',x2,y2)

# plt.subplot(212)
# plt.xlabel('x1-axis')
# plt.ylabel('y1-axis')
plt.show()

