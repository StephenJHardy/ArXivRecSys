from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime

def test_create_paper(client: TestClient, test_user_token):
    paper_data = {
        "arxiv_id": "2401.12345",
        "title": "Test Paper",
        "abstract": "This is a test paper abstract",
        "authors": "Test Author 1, Test Author 2",
        "categories": "cs.AI cs.LG",
        "published_date": datetime.utcnow().isoformat()
    }
    
    response = client.post(
        "/api/papers/",
        json=paper_data,
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data["arxiv_id"] == paper_data["arxiv_id"]
    assert data["title"] == paper_data["title"]
    assert "id" in data
    assert "score" in data

def test_get_papers(client: TestClient, test_user_token):
    response = client.get(
        "/api/papers/",
        headers=test_user_token
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_papers_pagination(client: TestClient, test_user_token):
    response = client.get(
        "/api/papers/?skip=0&limit=5",
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_get_paper_by_id(client: TestClient, test_user_token, db: Session):
    # First create a paper
    paper_data = {
        "arxiv_id": "2401.54321",
        "title": "Test Paper for Retrieval",
        "abstract": "This is a test paper abstract",
        "authors": "Test Author",
        "categories": "cs.AI",
        "published_date": datetime.utcnow().isoformat()
    }
    
    create_response = client.post(
        "/api/papers/",
        json=paper_data,
        headers=test_user_token
    )
    paper_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(
        f"/api/papers/{paper_id}",
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == paper_id
    assert data["arxiv_id"] == paper_data["arxiv_id"]

def test_get_nonexistent_paper(client: TestClient, test_user_token):
    response = client.get(
        "/api/papers/99999",
        headers=test_user_token
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Paper not found"

def test_rate_paper(client: TestClient, test_user_token, db: Session):
    # First create a paper
    paper_data = {
        "arxiv_id": "2401.98765",
        "title": "Test Paper for Rating",
        "abstract": "This is a test paper abstract",
        "authors": "Test Author",
        "categories": "cs.AI",
        "published_date": datetime.utcnow().isoformat()
    }
    
    create_response = client.post(
        "/api/papers/",
        json=paper_data,
        headers=test_user_token
    )
    paper_id = create_response.json()["id"]
    
    # Then rate it
    rating_data = {"rating": 5}
    response = client.post(
        f"/api/papers/{paper_id}/rate",
        json=rating_data,
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data["paper_id"] == paper_id
    assert data["rating"] == rating_data["rating"]

def test_rate_paper_invalid_score(client: TestClient, test_user_token):
    response = client.post(
        "/api/papers/1/rate",
        json={"rating": 6},  # Invalid rating > 5
        headers=test_user_token
    )
    assert response.status_code == 422  # Validation error 