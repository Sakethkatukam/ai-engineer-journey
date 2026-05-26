from functools import wraps
def func_logger(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print(f"[LOG] Calling {func.__name__} function")
        return func(*args,**kwargs)
    return wrapper


class Student:
    def __init__(self,fname,lname,age,location="Local")->None:
        self.fname=fname
        self.lname=lname
        self.age=age
        self.location=location
    
    def fullname(self)->str:
        return f"{self.fname} {self.lname}"
    
    @func_logger
    def details(self)->str:
        return f"This is {self.fullname()} and I am {self.age} years old"
    
    def change_location(self,new_location)->None:
        self.location=new_location
    
    def get_square(self,value)->int:
        for i in range(1,value+1):
            yield i**2
    

s1=Student("John","doe", 20)
print(s1.fullname())
print(s1.details())
s1.change_location("HYD")
print(s1.location)
# print(list(s1.get_square(4)))
for i in s1.get_square(4):
    print(i)