class College:
    def __init__(self,name,place):
        self.name = name
        self.place = place
        
    def profile_details(self):
        return {self.name,self.place}
    
clg1 = College("HOD","Hyderabad")
print clg1.profile_details()
    
    
class Staff(College):
    
    def __init__(self,subject):
        self.subject = subject
        
    def staff_profile(self):
        return {self.name,self.place,self.subject}
    
stf2  = Staff("Civics")
stf2.name = "pavan kota"
stf2.place = "New AP"
print "*****",stf2.staff_profile()

class Student(College):
    
    def __init__(self,std):
        self.std = std
        
    def student_profile(self):
        return {self.name,self.place,self.std}
    
std1 = Student(10)
std1.name="pavan"
std1.place = "andhra"
print std1.student_profile()

staff1 = Staff("History")
staff1.name = "Mrs.Indira"
staff1.place = "Andhra"
print staff1.staff_profile()
print "profile details of staff-------->",staff1.profile_details()
print "profile details of student-------->",std1.profile_details()
stf1 = isinstance(staff1, Student)
print stf1

a = isinstance(std1, College)
print a

a = isinstance(std1, Student)
print "std1 Student -->",a

a = isinstance(staff1, Student)
print "staff1 Student -->",a

a = isinstance(staff1, College)
print "staff1 College -->",a

a = isinstance(stf2,College)
print "stf2 College -->",a

a = isinstance(clg1,Student)
print "is clg1 an object of Student",a

a = isinstance(clg1,College)
print "is clg1 an object of College",a

a = isinstance(clg1,Staff)
print "is clg1 an object of Staff",a