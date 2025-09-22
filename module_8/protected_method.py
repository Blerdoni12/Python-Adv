class MyClass:
    def __init__(self):
        self._protected_variable = "this is a protected variable"

    def _protected_method(self):
        print("this is a protected method")

my_class = MyClass()
print(my_class._protected_variable)
my_class._protected_method()