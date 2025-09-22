class Rectangle:
    def __init__(self,length,width):
        self.length = length
        self.width = width
    def calculate_area(self):
        return self.length * self.width
    def calculate_perimeter(self):
        return 2*(self.length + self.width)

rectangle1 = Rectangle(100,5)
rectangle2 = Rectangle(50,20)

area = rectangle1.calculate_area()
perimeter = rectangle2.calculate_perimeter()

print(area)
print(perimeter)




















class Person:

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello,I am{self.name},and i am {self.age} years old")

person1 = Person("John", 15)
person2 = Person("Blerdon",16)

person1.greet()
person2.greet()

class Student:

    def __init__(self,name,age,course):
        self.name = name
        self.age = age
        self.course = course

student1 = Student ('Blerdon',15,'Python')
student2 = Student ('Amar',14,'Php')

print(student1.course)
print(student2.name)



