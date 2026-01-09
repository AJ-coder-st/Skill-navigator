"""
Authentication routes - Register, Login, User management
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from core.database import get_database
from core.auth import verify_password, get_password_hash, create_access_token, verify_token
from core.email_service import email_service

router = APIRouter()

# Request models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

# Dependency to get current user
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        database = get_database()
        user = await database["users"].find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/register")
async def register(request: RegisterRequest):
    """Register a new user"""
    # Validate password length
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    if len(request.password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot exceed 72 characters")
    
    database = get_database()
    users_collection = database["users"]
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    try:
        hashed_password = get_password_hash(request.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password hashing failed: {str(e)}")
    
    user_data = {
        "email": request.email,
        "password": hashed_password,
        "name": request.name,
        "created_at": datetime.utcnow(),
        "analyses": [],
        "roadmaps": []
    }
    
    result = await users_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(result.inserted_id), "email": request.email})
    
    # Send welcome email
    await email_service.send_email(
        request.email,
        "Welcome to Career Readiness Mentor!",
        f"""
        <html>
        <body>
            <h1>Welcome, {request.name}!</h1>
            <p>Thank you for joining Career Readiness Mentor. Start analyzing your skills and building your career path today!</p>
        </body>
        </html>
        """
    )
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(result.inserted_id),
            "email": request.email,
            "name": request.name
        }
    }

@router.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    database = get_database()
    users_collection = database["users"]
    
    # Find user
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["_id"]), "email": request.email})
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name", "")
        }
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "success": True,
        "user": {
            "id": str(current_user["_id"]),
            "email": current_user["email"],
            "name": current_user.get("name", ""),
            "created_at": current_user.get("created_at")
        }
    }
