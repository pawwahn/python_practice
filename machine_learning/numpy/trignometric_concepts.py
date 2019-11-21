import numpy as np
a = np.arange(0, 100)
print(a,"\n")
print('Sine of different angles:')
# Convert to radians by multiplying with pi/180

for i in a:
    print("Radians {} in degrees is : {}".format(i, np.sin(i*np.pi/180)))
print("------------")

for i in a:
    print("Radians {} in degrees is : {}".format(i, np.cosh(i*np.pi/180)))