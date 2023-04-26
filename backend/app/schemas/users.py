from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserBase):
    created_date: datetime


class UserCreate(UserBase):
    password: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "password": "ExAmplEpaSswOrd12",
                "is_admin": False,
                "first_name": "john",
                "last_name": "doe",
            }
        }


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: Optional[bool]


class TokenData(BaseModel):
    id: Optional[str] = None
