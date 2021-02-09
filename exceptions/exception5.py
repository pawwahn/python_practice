def divide(x, y):
    try:
        # Floor Division : Gives only Fractional
        # Part as Answer
        result = x // y
        print("Yeah ! Your answer is :", result)
    except ZeroDivisionError:
        print("Sorry ! You are dividing by zero ")

    # Look at parameters and note the working of Program
    else:
        print("No Exception raised")
    finally:
        print("finally printed")


divide(3, 2)
# divide(3, 0)