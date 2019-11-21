from matplotlib import pyplot as plt
import os
import re
import csv


#the_list=["Date","Open","High","Low","Close","Volume"]

# the_file = open("/home/likewise-open/HTCINDIA/pavankumark/Desktop/aapl.csv", 'w+')
# writer = csv.writer(the_file, delimiter='\t')
# writer.writerow(the_list)

my_file = open("/home/likewise-open/HTCINDIA/pavankumark/Desktop/aapl.csv", 'r')
reader = csv.reader(my_file, delimiter='\t')
#print reader
my_list = list(reader)
#print(my_list)

for i in my_list:
    print (i[0])