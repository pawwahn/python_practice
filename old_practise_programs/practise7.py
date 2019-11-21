class Employee:
    
#     def __init__(self,name,age):
#        self.name = name
#        self.age = age
#        
# #     def __str__(self):
# #         pass
#        
#     def get_details(self):
#         lists = [self.name , self.age]
#         return lists
#     
#     def update_details(self):
#         print "called **"
#         print "self **",self
#         
# e1 = Employee("pavan",25)
# print e1
# print e1.get_details()
# 
# print "update details -->",e1.update_details()


    def sum_check(self,a,b):
        print "called -===="
        self.a = a
        self.b = b
        sum_value = a + b
        return sum_value
    
    def __str__(self):
        pass
    
    
sum1 = Employee()
sum1.sum_check(5, 10)
print sum1


   