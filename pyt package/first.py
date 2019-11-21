print "This file1 will be run always"
print "From the first file: ", format(__name__)
def main():
    print "From the first file: ", format(__name__)

if __name__ == '__main__':
    main()