# https://www.w3resource.com/python-exercises/file/python-io-exercise-4.php

import sys
import os
def file_read_from_tail(fname,lines):
        bufsize = 832  # should be greater than file size
        fsize = os.stat(fname).st_size
        print("---- file size is : {}".format(fsize))
        iter = 0
        with open(fname) as f:
                if bufsize > fsize:
                        bufsize = fsize-1
                        data = []
                        while True:
                                iter +=1
                                f.seek(fsize-bufsize*iter)
                                data.extend(f.readlines())
                                if len(data) >= lines or f.tell() == 0:
                                        print(''.join(data[-lines:]))
                                        break

file_read_from_tail(fname='D:\pytohn_git_folder\searches\pavan.txt',lines=2)