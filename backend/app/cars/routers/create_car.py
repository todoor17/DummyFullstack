from fastapi import APIRouter, Security
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.auth import check_valid_token
from app.cars.model import Car
from app.cars.schemas import CreateCarRequest
from app.database import get_db

router = APIRouter()
security = HTTPBearer()

@router.post("/create-car", tags=["2. Cars"])
async def create_car(request: CreateCarRequest, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    check_valid_token(token, "ADMIN")

    car = Car(brand=request.brand, mileage=request.mileage, nr_of_seats=0, car_color=request.car_color, owner=request.owner)
    db.add(car)
    db.commit()
    db.refresh(car)

    return car