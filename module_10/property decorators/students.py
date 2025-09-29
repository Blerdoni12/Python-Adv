class Student:
    def __init__(self,name,age):
        self._name = name
        self._age = age
@property
def name(self):
    return self._name

@name.setter
def name(self,name):
    self._name = name

@property
def age(self):
    return self._age

@age.setter
def age (self):
    def name(self,age):
        self._age = age

student1 = Student("amar",67)

print("Name:",student1._name)
print("Age:",student1._age)

student1.name = "Dombosko"
student1.age = 41

print("Updated name:",student1.name)
print("Updated age:",student1.age)

