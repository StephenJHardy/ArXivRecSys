from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class PaperBase(BaseModel):
    arxiv_id: str
    title: str
    abstract: str
    authors: str
    categories: str
    published_date: date
    score: float

class Paper(PaperBase):
    id: int

    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    rating: int

class Rating(RatingBase):
    id: int
    user_id: int
    paper_id: int

    class Config:
        from_attributes = True 