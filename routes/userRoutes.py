from database.db import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.userModels import UserSchema, ShowUser, Token, AnswerSchema
from sqlalchemy.orm import Session
from typing import List
from auth.authenticate import authenticate
from pydantic import EmailStr


from controllers import userControllers

user_router = APIRouter(
    tags=["User"],
)

@user_router.post("/signup")
def sign_user_up(request: UserSchema, db : Session = Depends(get_db)) -> dict:
    return userControllers.sign_up(request, db)


@user_router.post("/signin", response_model=Token)
def sign_user_in(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> dict:
    return userControllers.sign_in(request, db)

@user_router.get("/", response_model=List[ShowUser])
def get_user_list(db : Session = Depends(get_db), user: UserSchema = Depends(authenticate)) -> dict:
    return userControllers.get_all_user(db)

@user_router.get("/{id}", response_model=ShowUser)
def get_a_user(id: int, db : Session = Depends(get_db), user: UserSchema = Depends(authenticate)) -> dict:
    return userControllers.get_user(id, db)

@user_router.put("/get-health-condition")
def analyze_my_health_condition(request: AnswerSchema, db : Session = Depends(get_db), user: UserSchema = Depends(authenticate)) -> dict:
    return userControllers.analysis_health_condition(request, db)