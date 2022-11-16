from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)

    class Config:
        schema_extra = {
            "Contoh": {
                "email": "contoh123@mailmail.com",
                "password": "ashiapp!!",
            }
        }

class UserSchema(BaseModel):
    email:EmailStr
    password:str

    class Config:
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
                "password": "ashiapp!!",
            }
        }

class ShowUser(BaseModel):
    email:EmailStr

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None