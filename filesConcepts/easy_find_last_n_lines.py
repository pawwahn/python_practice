def lastNLines(file, n):
    with open(file) as file:
        print("last {} lines of the file are:".format(n))
        for line in (file.readlines()[-n:]):
            print(line, end='')

lastNLines(file='D:\pytohn_git_folder\searches\pavan.txt',n=2)