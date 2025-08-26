from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.users.model import User

router = APIRouter()

@router.get("/users", description="Retrieve all users", status_code=status.HTTP_200_OK, tags=["1. Users"])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
