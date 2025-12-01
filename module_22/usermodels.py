from pydantic import BaseModel, conint, constr
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    age: int = 0
    email: str = "noemail@example.com"

user1 = User(id=2, name="John Doe", email="johndoe@example.com")
print(user1)

user2 = User(id=3, name="John Doe", age=25)
print(user2)

user3 = User(id=4, name="John Doe", )
print(user3)

class another_user(BaseModel):
    id: conint(gt=0)
    name: constr(min_length=2, max_length=50)

valid_user = another_user(id=1, name="Alice")
print(valid_user)
