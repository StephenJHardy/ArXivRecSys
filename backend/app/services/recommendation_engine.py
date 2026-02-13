from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from app import models
from collections import defaultdict

def calculate_paper_scores(db: Session) -> Dict[int, float]:
    """
    Calculates scores for papers based on user ratings
    Currently using a simple average rating system
    """
    ratings = db.query(
        models.Rating.paper_id,
        func.avg(models.Rating.rating).label('avg_rating'),
        func.count(models.Rating.id).label('rating_count')
    ).group_by(models.Rating.paper_id).all()
    
    scores = {}
    for paper_id, avg_rating, rating_count in ratings:
        # Simple scoring formula: average rating weighted by number of ratings
        score = avg_rating * (1 - 1/(rating_count + 1))
        scores[paper_id] = score
    
    return scores

def get_user_preferences(db: Session, user_id: int) -> Dict[str, float]:
    """
    Analyzes user's ratings to determine their preferences for different categories
    """
    user_ratings = db.query(
        models.Rating.rating,
        models.Paper.categories
    ).join(
        models.Paper,
        models.Rating.paper_id == models.Paper.id
    ).filter(
        models.Rating.user_id == user_id
    ).all()
    
    category_scores = defaultdict(list)
    for rating, categories in user_ratings:
        for category in categories.split():
            category_scores[category].append(rating)
    
    preferences = {}
    for category, ratings in category_scores.items():
        avg_rating = sum(ratings) / len(ratings)
        preferences[category] = avg_rating
    
    return preferences

def get_personalized_recommendations(
    db: Session,
    user_id: int,
    limit: int = 10
) -> List[models.Paper]:
    """
    Gets personalized paper recommendations for a user
    Currently using a simple category-based approach
    """
    preferences = get_user_preferences(db, user_id)
    if not preferences:
        # If no preferences yet, return highest rated papers
        return db.query(models.Paper).order_by(
            models.Paper.score.desc()
        ).limit(limit).all()
    
    # Get papers and calculate a personalized score based on user preferences
    papers = db.query(models.Paper).all()
    paper_scores = []
    
    for paper in papers:
        score = paper.score
        # Boost score based on matching categories
        for category in paper.categories.split():
            if category in preferences:
                score *= (1 + preferences[category] / 5)  # Normalize by max rating
        paper_scores.append((paper, score))
    
    # Sort papers by personalized score and return top results
    paper_scores.sort(key=lambda x: x[1], reverse=True)
    return [paper for paper, _ in paper_scores[:limit]] 