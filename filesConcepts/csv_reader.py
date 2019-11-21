import os
import csv

#print os.getcwd()
with open('Z:\learnings python\\files\\file1.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #for line in csv_reader:
    #    print "line ",line
    with open('Z:\learnings python\\files\\file3.txt','a') as new_file:
        #csv_writer = csv.writer(new_file, delimiter='-')
        for line in csv_reader:
            print "line ",line
            for l in line:
                new_file.write(l)

    #print csv_reader
    #next(csv_reader)        # skips 1st line of the csv file
    #next(csv_reader)       # skips the 2nd  line of the csv file

    #for line in csv_reader:
    #    print line[2]

    for line in csv_reader:
        print line

        #csv_writer.writerow(line)

    new_file.close()