def divs(a,b):
    try:
        print(a/b)
    except Exception as e:
        print("Not divisible")
    finally:
        print("Inside finally")

divs(10,1)

