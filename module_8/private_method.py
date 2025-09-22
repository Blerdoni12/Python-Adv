class MyClass:
    def __init__(self):
        self.__private_variable = "this is a private variable"

    def __private_method(self):
        print("this is a private method")

my_class = MyClass()
print(my_class._MyClass__private_variable)
my_class._MyClass__private_method()
