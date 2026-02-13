from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional

def get_paper(db: Session, paper_id: int) -> Optional[models.Paper]:
    return db.query(models.Paper).filter(models.Paper.id == paper_id).first()

def get_paper_by_arxiv_id(db: Session, arxiv_id: str) -> Optional[models.Paper]:
    return db.query(models.Paper).filter(models.Paper.arxiv_id == arxiv_id).first()

def get_papers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Paper]:
    return db.query(models.Paper).offset(skip).limit(limit).all()

def create_paper(db: Session, paper: schemas.PaperCreate) -> models.Paper:
    db_paper = models.Paper(
        arxiv_id=paper.arxiv_id,
        title=paper.title,
        abstract=paper.abstract,
        authors=paper.authors,
        categories=paper.categories,
        published_date=paper.published_date
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def rate_paper(db: Session, paper_id: int, rating: schemas.RatingCreate) -> models.Rating:
    db_rating = models.Rating(
        paper_id=paper_id,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def update_paper_score(db: Session, paper_id: int, new_score: float) -> models.Paper:
    paper = get_paper(db, paper_id)
    if paper:
        paper.score = new_score
        db.commit()
        db.refresh(paper)
    return paper 