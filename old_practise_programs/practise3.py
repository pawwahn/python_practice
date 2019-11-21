#What is the function to randomize the items of a list in-place?

"""
Ans: Python has a built-in module called as <random>. It exports a public method <shuffle(<list>)> which can randomize any input sequence.

"""

import random
list = [2, 18, 8, 4]

tup = (2,4,5,6,8,7)
print "Prior Shuffling - 0", list
random.shuffle(list)
print "After Shuffling - 1", list
random.shuffle(list)
print "After Shuffling - 2", list