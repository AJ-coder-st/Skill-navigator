"""Database connection and utilities"""

from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
import json
import os

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return db.client[settings.DATABASE_NAME]

async def init_database():
    """Initialize database with sample data if collections are empty"""
    database = get_database()
    
    # Check if collections exist and have data
    job_descriptions = database["job_descriptions"]
    courses = database["courses"]
    
    job_count = await job_descriptions.count_documents({})
    course_count = await courses.count_documents({})
    
    # Load sample data if collections are empty
    if job_count == 0:
        sample_jds_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_job_descriptions.json")
        if os.path.exists(sample_jds_path):
            with open(sample_jds_path, "r") as f:
                sample_jds = json.load(f)
                if sample_jds:
                    await job_descriptions.insert_many(sample_jds)
                    print(f"Loaded {len(sample_jds)} sample job descriptions")
    
    if course_count == 0:
        sample_courses_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_courses.json")
        if os.path.exists(sample_courses_path):
            with open(sample_courses_path, "r") as f:
                sample_courses = json.load(f)
                if sample_courses:
                    await courses.insert_many(sample_courses)
                    print(f"Loaded {len(sample_courses)} sample courses")
