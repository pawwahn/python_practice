def outer_fun():
    message = "Hi"

    def inner_fun():
        print (message)
        #return True
    return inner_fun()

my_res = outer_fun()
print (my_res)