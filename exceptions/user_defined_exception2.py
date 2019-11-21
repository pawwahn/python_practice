class Error(Exception):
    """Base class from exception"""
    pass

class TooSmallNumber(Error):
    """Too small number inherited from """
    pass

class TooLargeNumber(Error):
    """Too large number inherited from """
    pass

num = 10
attempts = 0


while True:
    attempts += 1
    if attempts <= 3:
        ur_num = int(input("Enter your number :"))
        try:
            if ur_num < num:
                raise TooSmallNumber
            elif ur_num > num:
                raise TooLargeNumber
            break
        except TooSmallNumber:
            print("Your value is too small. Try again !!")
        except TooLargeNumber:
            print("Your value is too large. Try again !!")
    else:
        print("Your have utilized all your chances")
        break
print("You guess is correct in {} attempts".format(attempts))



#print("You guess is correct in {} attempts".format(attempts))


