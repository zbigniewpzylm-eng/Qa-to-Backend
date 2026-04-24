from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import Base, User


def get_user_by_id(user_id: int, db: Session):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def create_user(user_data: dict, db: Session):
    user = User(
    email=user_data["email"],
    name=user_data["name"],
    metadata_=user_data.get("metadata")
)  
    
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, detail="Email already exists")
    db.refresh(user)
    return user

    