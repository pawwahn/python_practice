# linear graphs
from matplotlib import pyplot as plt
from pychart.font import line_width
from pychart.pychart_util import label_desc



x = [1,2,3,4,5,6]
y = [1.1,-0.9,3.1,5.2,4.8,4.2]
y1 = [1,2,3,4,5,6]
x1 = [1.1,-0.9,3.1,5.2,4.8,4.2]


plt.plot(x,y,'pink',label='Line One')
plt.plot(x1,y1,'y',label='Line Two')
plt.legend()   
#plt.box('on') 
plt.title('Graphical Information',color='b')
plt.grid(b=None, which='major', axis='both')
plt.ylabel('Y Axis')
plt.xlabel('X Axis')


plt.show()