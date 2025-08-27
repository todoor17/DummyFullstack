import os
from datetime import timedelta, datetime
from operator import truediv

from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from jose import jwt, ExpiredSignatureError, JWTError

from app.users.model import User

SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("JWT_ALG")

security = HTTPBearer()


def create_jwt_token(user: User, expires_delta: timedelta):
    to_encode = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }

    expires = datetime.now() + expires_delta
    to_encode.update({"exp": expires})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def check_valid_token(token: str, role: str) -> dict:
    try:
        decoded = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    print(decoded)

    if decoded["role"] != role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have permission to do this")

    return decoded
