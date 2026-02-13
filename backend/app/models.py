from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    ratings = relationship("Rating", back_populates="user")

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True)
    title = Column(String)
    abstract = Column(Text)
    authors = Column(String)
    categories = Column(String)
    published_date = Column(DateTime)
    score = Column(Float, default=0.0)
    ratings = relationship("Rating", back_populates="paper")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    paper_id = Column(Integer, ForeignKey("papers.id"))
    rating = Column(Integer)  # 0-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="ratings")
    paper = relationship("Paper", back_populates="ratings") 