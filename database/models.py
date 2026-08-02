from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_id = Column(String, nullable=False)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
