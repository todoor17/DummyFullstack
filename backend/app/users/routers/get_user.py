from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.users.model import User

router = APIRouter()

@router.get("/users/{user_id}", description="Retrieve a specific user from the database", status_code=status.HTTP_200_OK, tags=["1. Users"])
async def get_user(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    specific_user = db.query(User).filter(User.id == user_id).first()

    if not specific_user:
        raise HTTPException(status_code=404, detail="User not found")

    return specific_user
