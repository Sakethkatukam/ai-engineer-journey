from datetime import datetime
class Employee:
    raise_amount = 1.04
    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary
    
    @staticmethod
    def is_workday(day):
        if day.weekday()==5 or day.weekday()==6:
            return False
        return True

    @classmethod
    def from_string(cls, emp_str):
        first,last,salary=emp_str.split("-")
        return cls(first, last, int(salary))

    def full_name(self):
        return "{} {}".format(self.first, self.last)

    def apply_raise(self):
        self.salary=int(self.salary*self.raise_amount)
    
    def print_email(self):
        print("{}.{}@company.com".format(self.first,self.last))

class Developer(Employee):
    language = "Python"
    def __init__(self,first,last,salary,language):
        super().__init__(first,last,salary)
        self.language = language

    def print_language(self):
        print("{}".format(self.language))
    
class Manager(Employee):
    def __init__(self,first,last,salary,employees=None):
        super().__init__(first,last,salary)
        if employees is None:
            self.employees = []
        else:
            self.employees=employees
    
    def add_employee(self,emp):
        self.employees.append(emp)
    
    def remove_employee(self,emp):
        self.employees.remove(emp)
    
# emp1 = Employee("John", "Doe", 50000)
emp_str_1="John-Doe-70000"
emp1=Employee.from_string(emp_str_1)
# print(emp1.full_name())
emp1.apply_raise()
print(emp1.salary)
# print(emp1.is_workday(datetime(2026,5,2)))
# emp1.print_email()
# mgr1=Manager("J","Smith",90000,[emp1])
# print(mgr1.full_name())
# dev1=Developer("Jane","Doe",60000,"Java")
# print(dev1.full_name()+' -> '+dev1.language)