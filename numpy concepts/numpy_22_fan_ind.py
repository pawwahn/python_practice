import numpy as np

a = np.arange(12).reshape(3,4)
print a,"\n"

z = a[[1,0,2], 2:  ]
#      rows     columns
print z,"\n"



z1 = a[[1,0,2], :3  ]
#      rows     columns
print z1,"\n"


z2 = a[[1,1,2], :3  ]
#      rows     columns
print z2,"\n"

z3 = a[[1], 2:4  ]
#      rows     columns
print z3,"\n"                               # [[6 7]] 