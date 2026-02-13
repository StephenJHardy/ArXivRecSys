from datetime import datetime
from app.services import recommendation_engine
from app import models

def test_calculate_paper_scores(db):
    # Create test papers
    paper1 = models.Paper(
        arxiv_id="2401.11111",
        title="Test Paper 1",
        abstract="Abstract 1",
        authors="Author 1",
        categories="cs.AI",
        published_date=datetime.utcnow()
    )
    paper2 = models.Paper(
        arxiv_id="2401.22222",
        title="Test Paper 2",
        abstract="Abstract 2",
        authors="Author 2",
        categories="cs.LG",
        published_date=datetime.utcnow()
    )
    db.add(paper1)
    db.add(paper2)
    db.commit()

    # Create test ratings
    ratings = [
        models.Rating(paper_id=paper1.id, rating=5),
        models.Rating(paper_id=paper1.id, rating=4),
        models.Rating(paper_id=paper2.id, rating=3)
    ]
    for rating in ratings:
        db.add(rating)
    db.commit()

    scores = recommendation_engine.calculate_paper_scores(db)
    
    assert paper1.id in scores
    assert paper2.id in scores
    assert scores[paper1.id] > scores[paper2.id]  # Paper1 has higher ratings

def test_get_user_preferences(db):
    # Create test user
    user = models.User(
        email="test@example.com",
        hashed_password="dummy_hash"
    )
    db.add(user)
    db.commit()

    # Create test papers with different categories
    papers = [
        models.Paper(
            arxiv_id="2401.33333",
            title="AI Paper",
            abstract="Abstract",
            authors="Author",
            categories="cs.AI",
            published_date=datetime.utcnow()
        ),
        models.Paper(
            arxiv_id="2401.44444",
            title="ML Paper",
            abstract="Abstract",
            authors="Author",
            categories="cs.LG",
            published_date=datetime.utcnow()
        )
    ]
    for paper in papers:
        db.add(paper)
    db.commit()

    # Create ratings with different scores for different categories
    ratings = [
        models.Rating(user_id=user.id, paper_id=papers[0].id, rating=5),  # AI paper
        models.Rating(user_id=user.id, paper_id=papers[1].id, rating=3)   # ML paper
    ]
    for rating in ratings:
        db.add(rating)
    db.commit()

    preferences = recommendation_engine.get_user_preferences(db, user.id)
    
    assert "cs.AI" in preferences
    assert "cs.LG" in preferences
    assert preferences["cs.AI"] > preferences["cs.LG"]

def test_get_personalized_recommendations(db):
    # Create test user
    user = models.User(
        email="test@example.com",
        hashed_password="dummy_hash"
    )
    db.add(user)
    db.commit()

    # Create several test papers
    papers = [
        models.Paper(
            arxiv_id=f"2401.{i}",
            title=f"Paper {i}",
            abstract=f"Abstract {i}",
            authors=f"Author {i}",
            categories="cs.AI" if i % 2 == 0 else "cs.LG",
            published_date=datetime.utcnow(),
            score=float(i)
        ) for i in range(1, 6)
    ]
    for paper in papers:
        db.add(paper)
    db.commit()

    # Create some ratings to establish preferences
    for i, paper in enumerate(papers[:3]):
        rating = models.Rating(
            user_id=user.id,
            paper_id=paper.id,
            rating=5 if paper.categories == "cs.AI" else 3
        )
        db.add(rating)
    db.commit()

    recommendations = recommendation_engine.get_personalized_recommendations(
        db, user.id, limit=3
    )
    
    assert len(recommendations) <= 3
    # Check if recommendations favor the preferred category
    ai_papers = [p for p in recommendations if "cs.AI" in p.categories]
    assert len(ai_papers) > 0 