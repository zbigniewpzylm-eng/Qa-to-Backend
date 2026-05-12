from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import User


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

def update_user(user_id: int,user_data_update: dict, db: Session,):
    # pobieram usera z db
    db_user = db.get(User, user_id)
    # zwracam 404 jak nie ma usera o takim ID
    if db_user is None:
        raise HTTPException(status_code= 404, detail="User Not found")
    #definiuje co ma byc zmienione
    update_data = user_data_update.model_dump(exclude_unset=True)
    #sprawdzam format danych i updejtuje usera
    
    if "email" in update_data:
        db_user.email = update_data["email"].lower()
    if "name" in update_data:
        db_user.name = update_data["name"]
    if "metadata" in update_data:
        db_user.metadata_ = {
            **(db_user.metadata_ or {}),
            **update_data["metadata"]
    }
        
    
    # próba commita razem z 409 jeśli dupli danych
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, detail="Email already exists")
    return db_user

def delete_user_by_id(user_id: int, db: Session):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db.delete(user)

    db.commit()
         