
try:
    file = open('dump.txt')
    var = 10
    #z = 10/1       # this is fro getting else part
    z = 10 / 0      # this is for getting ZeroDivisionException
except IOError as e:
    print("Sorry! File does not exists.")
except NameError as e:
    print("Name error occured")
except ZeroDivisionError as e:
    print("Zero Division Error occured")

else:
    print("Else part")
finally:
    print("Finally!!")
