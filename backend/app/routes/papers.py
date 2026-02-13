from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.controllers import paper_controller

router = APIRouter()

@router.get("/", response_model=List[schemas.Paper])
def get_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    papers = paper_controller.get_papers(db, skip=skip, limit=limit)
    return papers

@router.get("/{paper_id}", response_model=schemas.Paper)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = paper_controller.get_paper(db, paper_id=paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.post("/", response_model=schemas.Paper)
def create_paper(paper: schemas.PaperCreate, db: Session = Depends(get_db)):
    return paper_controller.create_paper(db=db, paper=paper)

@router.post("/{paper_id}/rate", response_model=schemas.Rating)
def rate_paper(
    paper_id: int,
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db)
):
    return paper_controller.rate_paper(db=db, paper_id=paper_id, rating=rating) 