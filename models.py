from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # ← This line is probably missing
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)