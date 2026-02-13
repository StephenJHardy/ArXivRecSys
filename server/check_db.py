from database import SessionLocal, engine, Base
from models import User, Paper, Rating

def check_db():
    db = SessionLocal()
    try:
        # Check users
        users = db.query(User).all()
        print("\nUsers in database:")
        for user in users:
            print(f"- {user.email}")

        # Check papers
        papers = db.query(Paper).all()
        print("\nPapers in database:")
        if papers:
            for paper in papers:
                print(f"\nTitle: {paper.title}")
                print(f"Date: {paper.published_date}")
                print(f"Authors: {paper.authors}")
                print("-" * 50)
        else:
            print("No papers found in database!")

    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db() 