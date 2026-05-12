from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    metadata_ = Column(JSON, nullable=True)
