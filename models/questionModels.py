from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    masalah = Column(String)
    pilihan = Column(String)

    class Config:
        schema_extra = {
            "Contoh": {
                "masalah": "Kurang berminat atau bergairah dalam melakukan apapun",
                "pilihan": "0 (Tidak Pernah), 1 (Beberapa Hari), 2 (Lebih Dari 1 Minggu), 3 (Hampir Setiap Hari)"
            }
        }


class QuestionSchema(BaseModel):
    masalah: str
    pilihan: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "masalah": "Kurang berminat atau bergairah dalam melakukan apapun",
                "pilihan": "0 (Tidak Pernah), 1 (Beberapa Hari), 2 (Lebih Dari 1 Minggu), 3 (Hampir Setiap Hari)"
            }
        }


class QuestionShow(BaseModel):
    id: int
    masalah: str
    pilihan: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "int": 1,
                "masalah": "Kurang berminat atau bergairah dalam melakukan apapun",
                "pilihan": "0 (Tidak Pernah), 1 (Beberapa Hari), 2 (Lebih Dari 1 Minggu), 3 (Hampir Setiap Hari)"
            }
        }


class QuestionUpdate(BaseModel):
    masalah: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "masalah": "Kurang berminat atau bergairah dalam melakukan apapun",
            }
        }
