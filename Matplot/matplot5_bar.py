from matplotlib import pyplot as plt

x = [1,3,5,7,9]
y = [2,3,4,6,5]
x1 = [1.5,4,6,8,12]
y1 = [4,5,2,3,6]

plt.plot(x,y)
plt.plot(x1,y1)
plt.bar(x,y,label="Example 1",color='b')
plt.bar(x1,y1,label="Example 2",color='g')
plt.legend()
plt.title('Bar Graph View',color='r')
plt.xlabel('X - axis')
plt.ylabel('Y- axis')
plt.grid(b=None, which='major', axis='both')




plt.show()