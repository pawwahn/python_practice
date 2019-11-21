class Employee:
    __count = 10

    def __init__(self):
        Employee.__count = Employee.__count+1

    def display(self):
        print("The number of employees",Employee.__count)

    def __secured(self):
        print("Inside secured function..")

    def get_count(self):
        print("Employee count is :",Employee.__count)

emp = Employee()
emp2 = Employee()
print(Employee.__dict__)
print(Employee()._Employee__secured())
print(Employee()._Employee__count)
print("The private variable is : {}".format(Employee._Employee__count))

try:
    print(emp.__count)  # can not access the private values directly even with the help of class or its object.. one can acheive it by using functions
    #print(Employee().get_count())
except Exception as e:
    print("Exception is : {}".format(e))
finally:
    emp.display()

#################################
class A:
    __dummy = 10
    dummy = 100

    print(dummy)
    #print(_dummy)       # u can not directly access __dummy value
    #print(A().__dummy)   # u can not directly create an object and call the private variables

    def display_dummy(self):
        print(A.__dummy)
A().display_dummy()