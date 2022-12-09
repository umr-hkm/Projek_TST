from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    nama = Column(String)
    password = Column(String)
    diagnosis = Column(String, default="")
    severity = Column(String, default="")
    personality = Column(String, default="")

    class Config:
        schema_extra = {
            "Contoh": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus",
                "password": "ashiapp!!",
            }
        }


class UserSchema(BaseModel):
    email: EmailStr
    nama: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus",
                "password": "ashiapp!!",
            }
        }


class ShowUser(BaseModel):
    email: EmailStr
    nama: str
    diagnosis: str
    severity: str
    personality: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "contoh123@mailmail.com",
                "nama": "Agus",
                "diagnosis": "Major Depressive Disorder",
                "severity": "Severe",
                "personality" : "ENFP (Akurasi: 90%)"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class AnswerSchema(BaseModel):
    jawaban_masalah_1: conint(gt=-1, lt=4)
    jawaban_masalah_2: conint(gt=-1, lt=4)
    jawaban_masalah_3: conint(gt=-1, lt=4)
    jawaban_masalah_4: conint(gt=-1, lt=4)
    jawaban_masalah_5: conint(gt=-1, lt=4)
    jawaban_masalah_6: conint(gt=-1, lt=4)
    jawaban_masalah_7: conint(gt=-1, lt=4)
    jawaban_masalah_8: conint(gt=-1, lt=4)
    jawaban_masalah_9: conint(gt=-1, lt=4)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "jawaban_masalah_1": 0,
                "jawaban_masalah_2": 1,
                "jawaban_masalah_3": 0,
                "jawaban_masalah_4": 2,
                "jawaban_masalah_5": 0,
                "jawaban_masalah_6": 3,
                "jawaban_masalah_7": 0,
                "jawaban_masalah_8": 1,
                "jawaban_masalah_9": 2

            }
        }
