import os
from datetime import timedelta, datetime
from typing import Annotated

import bcrypt
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import create_jwt_token
from app.database import get_db

from starlette import status

from app.users.model import User
router = APIRouter()

SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("JWT_ALG")


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    if not bcrypt.checkpw(user.password.encode("utf-8"), hashed_password):
        print("Wrong password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return user


@router.post("/login", status_code=status.HTTP_200_OK, tags=["2. Login"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    token = create_jwt_token(user, expires_delta=timedelta(minutes=1))
    return {"user": user, "token": token}
