import os
from datetime import timedelta, datetime
from typing import Annotated

import bcrypt
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db

from starlette import status

from app.users.model import User
from jose import jwt
router = APIRouter()

SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("JWT_ALG")

print(SECRET_KEY)
print(ALGORITHM)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    if not bcrypt.checkpw(user.password.encode("utf-8"), hashed_password):
        print("Wrong password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta = None):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now() + expires_delta

    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

@router.post("/login", status_code=status.HTTP_200_OK, tags=["2. Login"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    token = create_access_token(username=form_data.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=1))
    return {"user": user, "token": token}
