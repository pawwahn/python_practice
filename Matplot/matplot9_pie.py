from matplotlib import pyplot as plt

slices = [7,2,8,6]
acts = ['sleep','eat','work','play']
clrs = ['m','c','r','pink']
exp = [0,0.1,0,0.2]

plt.pie(slices,labels=acts,colors=clrs,startangle=45,shadow=True,explode=exp,autopct='%1.2f%%')
plt.title("Pie-Chart")
plt.show()


"""
explode is for bring a part of one graph to outside
autopct is for showing number of digits in float
if colors=None is given, python generates its own default colors
if labels=None is given, labels are not displayed on the graph


"""