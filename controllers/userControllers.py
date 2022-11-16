from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.userModels import User, UserSchema
from fastapi import HTTPException, status
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token

def sign_up(request: UserSchema, db: Session):
    user= db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email sudah digunakan!"
        )
    
    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email = request.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "Pesan": "Akun berhasil dibuat!"
    }

def sign_in(request, db: Session):
    user= db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Akun dengan email tersebut tidak ditemukan."
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Gagal, silahkan periksa email/password Anda kembali!")
        
    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}

    

def get_all_user(db:Session):
    return db.query(User).all()