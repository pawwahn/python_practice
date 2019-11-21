from matplotlib import pyplot as plt

x = [4,5,2,1,6,4]
y = [5,1,4,9,6,7]

plt.scatter(x,y,label='Scatter',color='b')
plt.legend()
plt.grid(b=None,which='major',axis='both')
plt.show()