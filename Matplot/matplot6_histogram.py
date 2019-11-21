from matplotlib import pyplot as plt

population_ages =[4,4,6,18,50,21,15,9,22,25,29,88,102,78,88,65,64,25,95,1,52,20,9,19,18,15,19,21,20,22,22,29,24,27,28,24,25,25,45,55,46,43,25,15,15,19,34,35,61,34,75,77,70,72,79]
ages = [0,10,20,30,40,50,60,70,80,90,100,110,]

plt.hist(population_ages,ages,rwidth=0.9,label="Pop vs Age",color="blue")
#plt.hist(ages,population_ages,rwidth=0.9,label="Pop vs Age",color="pink")
#plt.plot(population_ages,ages)                                    # will not work as x and y do not have same dimensions

plt.xlabel("Ages",color="g")
plt.ylabel("Population Ages",color="b")
plt.legend()        # this is for showing the label..
plt.title("Histogram",color="r")
plt.grid(b=None, which='major', axis='both')
plt.show()

