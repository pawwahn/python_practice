from matplotlib import pyplot as plt
#from pychart.fill_style import line_width

days = [0,1,2,3,4,5,6]

sleep =[7,6,8,6,7,8,7]
work = [9,10,11,9,9,8,10]
eat =  [2,2,3,1,2,2,2]
exercise = [1.5,1,1,1,1,1,1]
play  = [4,5,5,4,3,4,3]

plt.plot([],[],color='g',label='sleep',linewidth=3)
plt.plot([],[],color='b',label='work',linewidth=5)
plt.plot([],[],color='y',label='eat',linewidth=1)
plt.plot([],[],color='r',label='exercise',linewidth=5)
plt.plot([],[],color='pink',label='play',linewidth=5)

#plt.plot(color='pink',label='play',linewidth=5)
plt.title("Area Graph")
plt.xlabel('Days')
plt.ylabel('Duties')

plt.stackplot(days,sleep,work,eat,exercise,play,colors=['g','b','y','r','pink'])
#plt.stackplot(sleep,days,work,eat,exercise,play,colors=['g','b','y','r','pink'])
plt.legend()
plt.show()