"""
API Routes - FastAPI endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from agents.jd_parser import jd_parser
from agents.profile_analyzer import profile_analyzer
from agents.skill_gap_analyzer import skill_gap_analyzer
from agents.roadmap_planner import roadmap_planner
from agents.practice_generator import practice_generator
from agents.reflection_agent import reflection_agent
from agents.resume_analyzer import resume_analyzer
from core.database import get_database
from core.email_service import email_service
from core.evaluation_harness import evaluation_harness
from core.feedback_system import feedback_system
from core.resume_parser import resume_parser
from core.resume_jd_matcher import resume_jd_matcher
from api.auth import get_current_user
import json
import os
import tempfile
import aiofiles

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

class FeedbackRequest(BaseModel):
    roadmap_id: str
    relevance_rating: int  # 1-5
    course_realistic: bool
    what_missing: Optional[str] = None
    what_unnecessary: Optional[str] = None
    additional_comments: Optional[str] = None

class EvaluationRequest(BaseModel):
    skill_gap_result: Dict[str, Any]
    job_requirements: Dict[str, Any]
    user_profile: Dict[str, Any]

class ResumeMatchRequest(BaseModel):
    resume_profile: Dict[str, Any]
    job_requirements: Dict[str, Any]

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
    """Analyze skill gaps between job requirements and student profile - always returns 200 with valid JSON"""
    try:
        result = await skill_gap_analyzer.analyze(request.job_skills, request.student_profile)
        
        # Ensure result has required structure
        if not isinstance(result, dict):
            result = {}
        
        # Ensure arrays exist
        if "missing_skills" not in result:
            result["missing_skills"] = []
        if "partial_skills" not in result:
            result["partial_skills"] = []
        if "strong_skills" not in result:
            result["strong_skills"] = []
        
        # Ensure arrays are lists
        if not isinstance(result["missing_skills"], list):
            result["missing_skills"] = []
        if not isinstance(result["partial_skills"], list):
            result["partial_skills"] = []
        if not isinstance(result["strong_skills"], list):
            result["strong_skills"] = []
        
        # Check if this is a fallback response
        is_fallback = result.get("fallback", False)
        
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
        
        response = {
            "success": True,
            "data": result,
            "status": "partial_success" if is_fallback else "success",
            "message": "Skill gap analysis completed" + (" (using fallback - LLM unavailable)" if is_fallback else "")
        }
        
        print(f"Skill gap response: success={response['success']}, missing={len(result.get('missing_skills', []))}, partial={len(result.get('partial_skills', []))}, strong={len(result.get('strong_skills', []))}")
        
        return response
        
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Error in skill-gap: {error_detail}")
        print(traceback.format_exc())
        
        # Return 200 with error in response instead of 500
        return {
            "success": False,
            "status": "error",
            "message": f"Skill gap analysis failed: {error_detail}",
            "data": {
                "error": True,
                "message": error_detail,
                "fallback": True,
                "missing_skills": [],
                "partial_skills": [],
                "strong_skills": [],
                "overall_assessment": "Analysis unavailable due to error",
                "reasoning": f"Error occurred: {error_detail}"
            }
        }

@router.post("/generate-roadmap")
async def generate_roadmap(
    request: RoadmapRequest,
    authorization: Optional[str] = Header(None)
):
    """Generate learning roadmap with citations, validation, and safety filters"""
    try:
        result = await roadmap_planner.generate(request.skill_gaps, request.time_weeks)
        
        # Add feedback prompt
        result["feedback_prompt"] = feedback_system.generate_feedback_prompt()
        
        # Send email if user is authenticated
        if authorization:
            try:
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

@router.post("/evaluate-skill-gap")
async def evaluate_skill_gap(
    request: EvaluationRequest,
    authorization: Optional[str] = Header(None)
):
    """Evaluate accuracy of skill-gap analysis"""
    try:
        evaluation = evaluation_harness.evaluate_skill_gap_analysis(
            request.skill_gap_result,
            request.job_requirements,
            request.user_profile
        )
        
        return {
            "success": True,
            "data": evaluation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit-feedback")
async def submit_feedback(
    request: FeedbackRequest,
    authorization: Optional[str] = Header(None)
):
    """Submit user feedback for roadmap"""
    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        user = await get_current_user(authorization)
        user_id = str(user.get("_id", ""))
        
        feedback_data = {
            "relevance_rating": request.relevance_rating,
            "course_realistic": request.course_realistic,
            "what_missing": request.what_missing or "",
            "what_unnecessary": request.what_unnecessary or "",
            "additional_comments": request.additional_comments or ""
        }
        
        feedback_record = await feedback_system.collect_roadmap_feedback(
            user_id,
            request.roadmap_id,
            feedback_data
        )
        
        return {
            "success": True,
            "data": {"feedback_id": str(feedback_record.get("_id", ""))}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evaluation-challenges")
async def get_evaluation_challenges():
    """Get held-out evaluation challenges (separate from practice)"""
    try:
        eval_challenges_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "evaluation_challenges.json"
        )
        
        if os.path.exists(eval_challenges_path):
            with open(eval_challenges_path, "r") as f:
                challenges = json.load(f)
            return {
                "success": True,
                "data": challenges,
                "message": "Held-out evaluation challenges (for assessment only, not practice)"
            }
        else:
            return {
                "success": True,
                "data": [],
                "message": "No evaluation challenges available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback-summary/{roadmap_id}")
async def get_feedback_summary(roadmap_id: str):
    """Get aggregated feedback summary for a roadmap"""
    try:
        summary = await feedback_system.get_feedback_summary(roadmap_id)
        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume file (PDF, DOC, DOCX) - always returns 200 with valid JSON"""
    try:
        # Validate file format
        if not resume_parser.is_supported(file.filename):
            return {
                "success": False,
                "status": "error",
                "message": f"Unsupported file format. Supported: PDF, DOC, DOCX",
                "data": {
                    "error": True,
                    "message": f"Unsupported file format: {file.filename}"
                }
            }
        
        # Save uploaded file temporarily
        file_ext = os.path.splitext(file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Parse resume text
            resume_text = resume_parser.parse(tmp_path)
            
            # Analyze resume
            profile_result = await resume_analyzer.analyze(resume_text)
            
            is_fallback = profile_result.get("fallback", False)
            
            response = {
                "success": True,
                "data": profile_result,
                "status": "partial_success" if is_fallback else "success",
                "message": "Resume analysis completed" + (" (using fallback - LLM unavailable)" if is_fallback else "")
            }
            
            return response
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Error in upload-resume: {error_detail}")
        print(traceback.format_exc())
        
        return {
            "success": False,
            "status": "error",
            "message": f"Resume parsing failed: {error_detail}",
            "data": {
                "error": True,
                "message": error_detail,
                "fallback": True
            }
        }

@router.post("/match-resume-jd")
async def match_resume_jd(request: ResumeMatchRequest):
    """Match resume profile against job description with fair scoring - always returns 200 with valid JSON"""
    try:
        result = await resume_jd_matcher.match(request.resume_profile, request.job_requirements)
        
        is_fallback = result.get("fallback", False)
        
        # Ensure result has correct structure for new format
        match_percentage = result.get("match_percentage", 0)
        if isinstance(match_percentage, str):
            try:
                match_percentage = int(float(match_percentage))
            except:
                match_percentage = 0
        
        # Ensure match_percentage is never 0 unless absolutely no relevance
        matched_skills = result.get("matched_skills", [])
        partial_matches = result.get("partial_matches", [])
        if match_percentage == 0 and (matched_skills or partial_matches):
            match_percentage = max(15, len(matched_skills) * 10 + len(partial_matches) * 5)
        
        # Ensure match_level exists
        if "match_level" not in result:
            if match_percentage >= 80:
                match_level = "Strong"
            elif match_percentage >= 60:
                match_level = "Good"
            elif match_percentage >= 40:
                match_level = "Moderate"
            else:
                match_level = "Low"
            result["match_level"] = match_level
        
        # Ensure scoring_explanation exists
        if "scoring_explanation" not in result or not result.get("scoring_explanation"):
            result["scoring_explanation"] = f"Match score of {match_percentage}% ({result['match_level']}) based on {len(matched_skills)} exact skill matches and {len(partial_matches)} partial matches."
        
        result["match_percentage"] = match_percentage
        result.setdefault("matched_skills", [])
        result.setdefault("partial_matches", [])
        result.setdefault("missing_skills", [])
        
        response = {
            "success": True,
            "data": result,
            "status": "partial_success" if is_fallback else "success",
            "message": "Resume-JD matching completed" + (" (using fallback - LLM unavailable)" if is_fallback else "")
        }
        
        print(f"Resume-JD Match: {match_percentage}% ({result['match_level']}) - {len(matched_skills)} exact, {len(partial_matches)} partial matches")
        return response
        
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"Error in match-resume-jd: {error_detail}")
        print(traceback.format_exc())
        
        return {
            "success": False,
            "status": "error",
            "message": f"Resume-JD matching failed: {error_detail}",
            "data": {
                "error": True,
                "message": error_detail,
                "fallback": True,
                "match_percentage": 0,
                "match_level": "Low",
                "matched_skills": [],
                "partial_matches": [],
                "missing_skills": [],
                "scoring_explanation": "Matching unavailable due to error"
            }
        }
