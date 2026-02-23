from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    api_key: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    api_key: str