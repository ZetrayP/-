class Student:
    SCHOLARSHIP_Outstanding = 6000
    SCHOLARSHIP_OutstandingGrad = 8000
    SCHOLARSHIP = 4000
    SCHOLARSHIP_GRAD = 6000
    
    def __init__(self, full_name, age, group, average_score):
        self.full_name = full_name
        self.age = age
        self.group = group
        self.average_score = average_score
        
    def display_info(self):
        print(f"Full name: {self.full_name}, Age: {self.age}, Group: {self.group}")
        
    def scholarship_amount(self):
        if self.average_score >= 5:
            return SCHOLARSHIP_Outstanding if isinstance(self, Student) else SCHOLARSHIP_OutstandingGrad
        else:
            return SCHOLARSHIP if isinstance(self, Student) else SCHOLARSHIP_GRAD
        
    def compare_scholarship(self, other):
        if self.scholarship_amount() > other.scholarship_amount():
            return "This student has a larger scholarship."
        elif self.scholarship_amount() < other.scholarship_amount():
            return "This student has a smaller scholarship."
        else:
            return "Both students have the same scholarship amount."


class GraduateStudent(Student):
    def __init__(self, full_name, age, group, average_score, scientific_work):
        super().__init__(full_name, age, group, average_score)
        self.scientific_work = scientific_work
        
    def display_info(self):
        super().display_info()
        print(f"Scientific work: {self.scientific_work}")


student = Student("John Hamish Watson", 20, "group1", 4.8)
graduate_student = GraduateStudent("Sherlock Holmes", 23, "group2", 5.0, "Criminal Psychology")

student.display_info()
print(f"Scholarship amount: {student.scholarship_amount()} Rubles")
graduate_student.display_info()
print(f"Scholarship amount: {graduate_student.scholarship_amount()} Rubles")

print(student.compare_scholarship(graduate_student))