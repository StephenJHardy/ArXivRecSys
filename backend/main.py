from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import papers, users
from app.database import create_tables

app = FastAPI(title="ArXiv Recommendation System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(papers.router, prefix="/api/papers", tags=["papers"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to ArXiv Recommendation System API"} 