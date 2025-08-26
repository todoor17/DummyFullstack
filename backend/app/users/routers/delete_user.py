from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.users.model import User

router = APIRouter()

@router.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["1. Users"])
async def delete_a_user(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(target_user)
    db.commit()
