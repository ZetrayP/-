from sqlmodel import SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    email: EmailStr
    password: str

class UserUpdate(SQLModel):
    email: EmailStr
    password: str

class UserOut(SQLModel):
    id: int
    email: EmailStr
    access_token: str = None