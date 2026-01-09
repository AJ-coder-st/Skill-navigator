"""
API Routes - FastAPI endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from agents.jd_parser import jd_parser
from agents.profile_analyzer import profile_analyzer
from agents.skill_gap_analyzer import skill_gap_analyzer
from agents.roadmap_planner import roadmap_planner
from agents.practice_generator import practice_generator
from agents.reflection_agent import reflection_agent
from core.database import get_database
from core.email_service import email_service
from api.auth import get_current_user

router = APIRouter()

# Request/Response Models
class JobDescriptionRequest(BaseModel):
    job_description: str

class ProfileRequest(BaseModel):
    degree: Optional[str] = None
    skills: List[str] = []
    experience_level: str = "beginner"
    projects: Optional[List[str]] = []
    certifications: Optional[List[str]] = []

class SkillGapRequest(BaseModel):
    job_skills: Dict[str, Any]
    student_profile: Dict[str, Any]

class RoadmapRequest(BaseModel):
    skill_gaps: Dict[str, Any]
    time_weeks: int = 8

class PracticeRequest(BaseModel):
    roadmap: Dict[str, Any]
    role: str
    skill_gaps: Dict[str, Any]

class ProgressRequest(BaseModel):
    original_roadmap: Dict[str, Any]
    progress: Dict[str, Any]

@router.post("/analyze-jd")
async def analyze_jd(request: JobDescriptionRequest):
    """Parse job description into structured format - always returns 200 with valid JSON"""
    try:
        if not request.job_description or not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty")
        
        result = await jd_parser.parse(request.job_description)
        
        # Always return 200 OK, even if fallback was used
        is_fallback = result.get("fallback", False)
        
        response = {
            "success": True,
            "data": result,
            "status": "partial_success" if is_fallback else "success",
            "message": "JD analysis completed" + (" (using fallback - LLM unavailable)" if is_fallback else "")
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Error in analyze-jd: {error_detail}")
        print(traceback.format_exc())
        
        # Return 200 with error in response instead of 500
        return {
            "success": False,
            "status": "error",
            "message": f"JD analysis failed: {error_detail}",
            "data": {
                "error": True,
                "message": error_detail,
                "fallback": True,
                "role": "Unknown",
                "required_skills": [],
                "preferred_skills": [],
                "soft_skills": [],
                "experience_level": "mid",
                "education_requirements": "See job description",
                "key_responsibilities": [],
                "reasoning": "Fallback analysis due to error"
            }
        }

@router.post("/analyze-profile")
async def analyze_profile(request: ProfileRequest):
    """Analyze and normalize student profile - always returns 200 with valid JSON"""
    try:
        if not request.skills and not request.degree:
            raise HTTPException(status_code=400, detail="Profile must include at least skills or degree")
        
        profile_dict = request.dict()
        result = await profile_analyzer.analyze(profile_dict)
        
        # Always return 200 OK, even if fallback was used
        # Check if this is a fallback response
        is_fallback = result.get("fallback", False)
        
        response = {
            "success": True,
            "data": result,
            "status": "partial_success" if is_fallback else "success",
            "message": "Analysis completed" + (" (using fallback - LLM unavailable)" if is_fallback else "")
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Error in analyze-profile: {error_detail}")
        print(traceback.format_exc())
        
        # Return 200 with error in response instead of 500
        return {
            "success": False,
            "status": "error",
            "message": f"Analysis failed: {error_detail}",
            "data": {
                "error": True,
                "message": error_detail,
                "fallback": True
            }
        }

@router.post("/skill-gap")
async def analyze_skill_gap(
    request: SkillGapRequest,
    authorization: Optional[str] = Header(None)
):
    """Analyze skill gaps between job requirements and student profile"""
    try:
        result = await skill_gap_analyzer.analyze(request.job_skills, request.student_profile)
        
        # Send email if user is authenticated
        if authorization:
            try:
                from api.auth import get_current_user
                user = await get_current_user(authorization)
                jd_data = request.job_skills
                profile_data = request.student_profile
                await email_service.send_analysis_report(
                    user["email"],
                    user.get("name", "User"),
                    jd_data,
                    profile_data,
                    result
                )
            except:
                pass  # Don't fail if email sending fails
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-roadmap")
async def generate_roadmap(
    request: RoadmapRequest,
    authorization: Optional[str] = Header(None)
):
    """Generate learning roadmap"""
    try:
        result = await roadmap_planner.generate(request.skill_gaps, request.time_weeks)
        
        # Send email if user is authenticated
        if authorization:
            try:
                from api.auth import get_current_user
                user = await get_current_user(authorization)
                await email_service.send_roadmap(
                    user["email"],
                    user.get("name", "User"),
                    result
                )
            except:
                pass  # Don't fail if email sending fails
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-practice")
async def generate_practice(request: PracticeRequest):
    """Generate practice materials"""
    try:
        result = await practice_generator.generate(request.roadmap, request.role, request.skill_gaps)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-progress")
async def update_progress(request: ProgressRequest):
    """Reflect on progress and update roadmap"""
    try:
        result = await reflection_agent.reflect(request.original_roadmap, request.progress)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard-summary")
async def dashboard_summary():
    """Get dashboard summary statistics"""
    try:
        database = get_database()
        
        # Count documents in collections
        jd_count = await database["job_descriptions"].count_documents({})
        course_count = await database["courses"].count_documents({})
        
        return {
            "success": True,
            "data": {
                "job_descriptions": jd_count,
                "courses": course_count,
                "status": "operational"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
