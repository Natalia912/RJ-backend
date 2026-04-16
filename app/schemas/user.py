from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class User(UserBase):
    id: int
    hashed_password: str 

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserLogin(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int

class TokenData(BaseModel):
    email: EmailStr | None = None