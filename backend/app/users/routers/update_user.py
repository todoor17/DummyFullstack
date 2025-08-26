from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.users.model import User
from app.users.schemas import UserCreate

router = APIRouter()

@router.put("/update-user/{user_id}", status_code=status.HTTP_200_OK, tags=["1. Users"])
async def update_a_user(user_update: UserCreate, user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_username = db.query(User).filter(User.username == user_update.username).first()
    existing_email = db.query(User).filter(User.email == user_update.email).first()

    if existing_email or existing_username:
        raise HTTPException(status_code=409, detail="The value already exists")

    if user_update.username:
        target_user.username = user_update.username
    if user_update.email:
        target_user.email = user_update.email
    if user_update.password:
        target_user.password = user_update.password

    db.commit()
    db.refresh(target_user)

    return target_user