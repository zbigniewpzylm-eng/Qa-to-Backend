from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import declarative_base

Base = declarative_base()

Class User(Base):

__tablename__ = "user_account"

metadata,
("user", Column("id", Integer, primary_key=True, autoincrement=True),
Column("name", String, nullable=False),
Column("email", String, unique=True, nullable=False),
Column("metadata", JSON, nullable=True) )