from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaperBase(BaseModel):
    arxiv_id: str
    title: str
    abstract: str
    authors: str
    categories: str
    published_date: datetime

class PaperCreate(PaperBase):
    pass

class Paper(PaperBase):
    id: int
    score: float
    
    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    rating: int

class RatingCreate(RatingBase):
    paper_id: int

class Rating(RatingBase):
    id: int
    user_id: int
    paper_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 