"""
Career Readiness Mentor & Skill-Gap Navigator
FastAPI Backend - Main Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

from api.routes import router
from api.auth import router as auth_router
from core.config import settings
from core.database import connect_to_mongo, close_mongo_connection, init_database

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await connect_to_mongo()
        await init_database()
    except Exception as e:
        print(f"Warning: Database initialization issue: {str(e)}")
        print("Continuing without database - some features may be limited")
    
    yield
    
    # Shutdown - ensure clean disconnect
    try:
        await close_mongo_connection()
    except Exception as e:
        print(f"Warning during shutdown: {str(e)}")

app = FastAPI(
    title="Career Readiness Mentor API",
    description="AI-powered skill gap analysis and learning roadmap generator",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {
        "message": "Career Readiness Mentor API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Use reload=False to avoid multiprocessing issues on Windows
    # Or use reload="watchfiles" if watchfiles is installed
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        reload_delay=1.0  # Add delay to avoid rapid reloads
    )
