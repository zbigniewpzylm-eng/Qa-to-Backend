from database import engine
from models import Base, User
from database import SessionLocal
from sqlalchemy.orm import Session
#from fastapi import HTTPException
from services import get_user_by_id

Base.metadata.create_all(engine)


user = User(
    email="test1@test.com",
    name="Test",
    metadata_={"role": "admin"}
)

db = SessionLocal()


db.add(user)
db.commit()
db.refresh(user)

user = get_user_by_id(1, db)
print(user.email)