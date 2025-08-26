from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Header
from sqlalchemy.orm import Session
from starlette import status

from app.cars.model import Car
from app.cars.schemas import CreateCarRequest, CarBase
from app.database import get_db

from jose import jwt

import os

SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("JWT_ALG")
router = APIRouter()

def check_valid_token(token: str):
    decoded = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)

    if not decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not decoded["role"] == "ADMIN":
        raise HTTPException(status_code=401, detail="You don't have the rights to add a car")

    elif decoded["exp"] < datetime.now().timestamp():
        raise HTTPException(status_code=401, detail="Your token is expired. Login again")


@router.post("/create-car", tags=["2. Cars"])
async def create_car(request: CreateCarRequest, token: str = Header(...), db: Session = Depends(get_db)):
    check_valid_token(token)

    car = Car(brand=request.brand, mileage=request.mileage, nr_of_seats=0, car_color=request.car_color, owner=request.owner)
    db.add(car)
    db.commit()
    db.refresh(car)

    return car