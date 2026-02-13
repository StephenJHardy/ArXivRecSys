from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, date, timezone
from typing import Optional, List
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.types import Date
from database import get_db
from models import User, Paper, Rating
import schemas
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter
from sqlalchemy import func

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "development_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI app
app = FastAPI()

# Create API router with prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email)
    if user is None:
        raise credentials_exception
    return user

@api_router.post("/users/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}

@api_router.get("/users/me/ratings")
async def get_user_ratings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Get all ratings for the current user
        ratings = db.query(Rating).filter(Rating.user_id == current_user.id).all()
        
        # Format the ratings
        formatted_ratings = []
        for rating in ratings:
            formatted_rating = {
                "id": rating.id,
                "paper_id": rating.paper_id,
                "rating": rating.rating,
                "created_at": rating.created_at.isoformat() if rating.created_at else None
            }
            formatted_ratings.append(formatted_rating)
        
        return formatted_ratings
    except Exception as e:
        print(f"Error in get_user_ratings: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.get("/papers/dates")
async def get_paper_dates(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get list of dates that have papers with their counts"""
    try:
        print("Fetching paper dates...")  # Debug log
        # Get distinct dates and their paper counts
        date_counts = db.query(
            Paper.published_date,
            func.count(Paper.id).label('count')
        ).group_by(Paper.published_date)\
         .order_by(Paper.published_date.desc())\
         .all()
        
        print(f"Found {len(date_counts)} distinct dates")  # Debug log
        
        # Convert dates to string format and create response objects
        date_data = []
        for date_tuple in date_counts:
            if date_tuple[0] is not None:
                try:
                    date_obj = date_tuple[0]
                    if isinstance(date_obj, str):
                        # If it's a string, parse it first
                        date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
                    elif not isinstance(date_obj, date):
                        # If it's a datetime, convert to date
                        date_obj = date_obj.date()
                    
                    date_str = date_obj.strftime("%Y-%m-%d")
                    date_data.append({
                        "date": date_str,
                        "count": date_tuple[1]
                    })
                    print(f"Added date: {date_str} with {date_tuple[1]} papers")  # Debug log
                except Exception as e:
                    print(f"Error formatting date {date_tuple[0]}: {e}")  # Debug log
                    continue
        
        print(f"Returning {len(date_data)} formatted dates")  # Debug log
        return {"dates": date_data}  # Return as JSON object
    except Exception as e:
        print(f"Error in get_paper_dates: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.get("/papers/{date}", response_model=List[schemas.Paper])
async def get_papers_by_date(
    date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get papers for a specific date"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        print(f"Looking for papers on date: {target_date}")  # Debug log
        
        papers = db.query(Paper)\
                  .filter(Paper.published_date.cast(Date) == target_date)\
                  .order_by(Paper.score.desc())\
                  .all()
        print(f"Found {len(papers)} papers")  # Debug log
        return papers if papers else []
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Use YYYY-MM-DD: {str(e)}"
        )
    except Exception as e:
        print(f"Error in get_papers_by_date: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.get("/papers", response_model=List[schemas.Paper])
async def get_papers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all papers (to be deprecated)"""
    try:
        print("Fetching all papers...")  # Debug log
        papers = db.query(Paper)\
                  .order_by(Paper.published_date.desc(), Paper.score.desc())\
                  .all()
        print(f"Found {len(papers)} papers in total")  # Debug log
        if not papers:
            print("Warning: No papers found in database")  # Debug log
        return papers
    except Exception as e:
        print(f"Error in get_papers: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.post("/papers/{paper_id}/rate")
async def rate_paper(
    paper_id: int,
    rating_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rating_value = rating_data.get("rating_value")
    if rating_value is None:
        raise HTTPException(status_code=422, detail="rating_value is required in request body")
    
    if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
        raise HTTPException(status_code=400, detail="Rating must be an integer between 1 and 5")
    
    # Check if paper exists
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Check if user has already rated this paper
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.paper_id == paper_id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_value
    else:
        # Create new rating
        new_rating = Rating(
            user_id=current_user.id,
            paper_id=paper_id,
            rating=rating_value
        )
        db.add(new_rating)
    
    db.commit()
    return {"message": "Rating submitted successfully"}

# Create initial admin user if it doesn't exist
def create_initial_admin():
    db = next(get_db())
    if not get_user(db, "admin@example.com"):
        admin_user = User(
            email="admin@example.com",
            hashed_password=pwd_context.hash("admin123")
        )
        db.add(admin_user)
        db.commit()

# Create some initial papers if none exist
def create_initial_papers():
    db = next(get_db())
    if db.query(Paper).count() == 0:
        papers = [
            Paper(
                arxiv_id="2401.12345",
                title="Deep Learning Approaches in Recommendation Systems",
                abstract="This paper explores various deep learning approaches in modern recommendation systems...",
                authors="John Doe, Jane Smith",
                categories="cs.LG cs.AI",
                published_date="2024-01-15",
                score=0.0
            ),
            Paper(
                arxiv_id="2401.67890",
                title="Transformer Models for Scientific Paper Classification",
                abstract="We present a novel approach to scientific paper classification using transformer models...",
                authors="Alice Johnson, Bob Wilson",
                categories="cs.CL cs.AI",
                published_date="2024-01-15",
                score=0.0
            )
        ]
        for paper in papers:
            db.add(paper)
        db.commit()

# Include API router
app.include_router(api_router)

if __name__ == "__main__":
    create_initial_admin()
    create_initial_papers()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 