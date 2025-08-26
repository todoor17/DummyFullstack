from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.users.model import User
from app.users.schemas import UserCreate

import bcrypt

router = APIRouter()

@router.post("/create-user", status_code=status.HTTP_201_CREATED, tags=["1. Users"])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())

    password = new_user.password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    new_user.password = hashed_password

    existing_username = db.query(User).filter(User.username == new_user.username).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == new_user.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
