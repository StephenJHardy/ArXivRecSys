from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app import models
from app.services.recommendation_engine import calculate_paper_scores

def rank_daily_papers(db: Session, days_back: int = 1) -> List[models.Paper]:
    """
    Ranks papers from the last N days using a combination of:
    - Paper score (from user ratings)
    - Recency
    - Number of ratings
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
    
    # Get papers from the specified time period
    papers = db.query(models.Paper).filter(
        models.Paper.published_date >= cutoff_date
    ).all()
    
    # Calculate current scores
    paper_scores = calculate_paper_scores(db)
    
    # Calculate ranking scores
    ranked_papers = []
    for paper in papers:
        base_score = paper_scores.get(paper.id, 0)
        
        # Calculate time decay factor (newer papers get a boost)
        hours_old = (datetime.utcnow() - paper.published_date).total_seconds() / 3600
        time_decay = 1.0 / (1 + hours_old/24)  # Decay over 24 hours
        
        # Calculate final ranking score
        ranking_score = base_score * time_decay
        
        ranked_papers.append((paper, ranking_score))
    
    # Sort papers by ranking score
    ranked_papers.sort(key=lambda x: x[1], reverse=True)
    
    return [paper for paper, _ in ranked_papers]

def update_paper_scores(db: Session):
    """
    Updates the score field for all papers based on current ratings
    """
    scores = calculate_paper_scores(db)
    for paper_id, score in scores.items():
        paper = db.query(models.Paper).filter(models.Paper.id == paper_id).first()
        if paper:
            paper.score = score
    db.commit() 