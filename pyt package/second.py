import first

print "This file2 will be run always",__name__

def main():
    print "From the second file: ", format(__name__)

if __name__ == '__main__':
    main()

