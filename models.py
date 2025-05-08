from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # ← This line is probably missing
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    title = Column(String)  
    content = Column(String)
    filename = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
