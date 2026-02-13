from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models import User, Paper, Rating
from passlib.context import CryptContext

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    db = SessionLocal()
    try:
        # Add test user if it doesn't exist
        if not db.query(User).filter(User.email == "admin@example.com").first():
            test_user = User(
                email="admin@example.com",
                hashed_password=pwd_context.hash("admin123")
            )
            db.add(test_user)
            db.commit()

        # Add some test papers if none exist
        if db.query(Paper).count() == 0:
            # Create papers for the last 3 days
            for i in range(3):
                date = datetime.now().date() - timedelta(days=i)
                for j in range(3):  # 3 papers per day
                    paper = Paper(
                        arxiv_id=f"2401.{i:02d}{j:02d}v1",
                        title=f"Test Paper {i}.{j} for {date}",
                        abstract="This is a test abstract that spans multiple lines.\nIt contains some technical content and mathematical formulas.\nIt should demonstrate the text wrapping functionality.",
                        authors=f"Author One, Author Two, Author Three",
                        categories="cs.AI cs.LG",
                        published_date=date,
                        score=0.0
                    )
                    db.add(paper)
            db.commit()

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete.") 