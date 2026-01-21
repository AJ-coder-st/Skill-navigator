"""
Course Validator - Anti-Hallucination System
Validates courses against verified database and prevents hallucinated credentials
"""

from typing import List, Dict, Any, Optional
from core.database import get_database

# Verified platforms (whitelist)
VERIFIED_PLATFORMS = {
    "Coursera",
    "edX",
    "Udemy",
    "Google Career Certificates",
    "Microsoft Learn",
    "AWS Training",
    "LinkedIn Learning",
    "Pluralsight",
    "Codecademy",
    "freeCodeCamp"
}

class CourseValidator:
    """Validates courses against database and prevents hallucination"""
    
    def __init__(self):
        self._verified_courses_cache = None
    
    async def get_verified_courses_list(self) -> List[str]:
        """Get list of all verified course names from database"""
        if self._verified_courses_cache is None:
            database = get_database()
            courses_collection = database["courses"]
            all_courses = await courses_collection.find({}).to_list(length=1000)
            self._verified_courses_cache = [
                course.get("resource_name", "").lower().strip()
                for course in all_courses
                if course.get("resource_name")
            ]
        return self._verified_courses_cache
    
    async def validate_course(self, course_name: str, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a course against database
        
        Returns:
            {
                "valid": bool,
                "course_data": dict or None,
                "reason": str
            }
        """
        database = get_database()
        courses_collection = database["courses"]
        
        # Try exact match first
        query = {"resource_name": {"$regex": course_name, "$options": "i"}}
        if provider:
            query["provider"] = {"$regex": provider, "$options": "i"}
        
        course = await courses_collection.find_one(query)
        
        if course:
            return {
                "valid": True,
                "course_data": course,
                "reason": "Found in verified database"
            }
        
        # Check if provider is verified platform
        if provider and provider not in VERIFIED_PLATFORMS:
            return {
                "valid": False,
                "course_data": None,
                "reason": f"Provider '{provider}' not in verified platforms list"
            }
        
        # Check against verified courses list
        verified_list = await self.get_verified_courses_list()
        course_lower = course_name.lower().strip()
        
        if any(course_lower in verified.lower() or verified.lower() in course_lower 
               for verified in verified_list):
            return {
                "valid": True,
                "course_data": None,  # Similar match but not exact
                "reason": "Similar course found in database"
            }
        
        return {
            "valid": False,
            "course_data": None,
            "reason": "Course not found in verified database"
        }
    
    async def filter_valid_courses(self, courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out invalid/hallucinated courses"""
        valid_courses = []
        
        for course in courses:
            course_name = course.get("resource_name", "")
            provider = course.get("provider", "")
            
            validation = await self.validate_course(course_name, provider)
            
            if validation["valid"]:
                # Use validated course data if available
                if validation["course_data"]:
                    valid_courses.append(validation["course_data"])
                else:
                    valid_courses.append(course)
            else:
                print(f"⚠️ Course rejected: {course_name} ({provider}) - {validation['reason']}")
        
        return valid_courses
    
    def is_verified_platform(self, provider: str) -> bool:
        """Check if provider is in verified platforms list"""
        return provider in VERIFIED_PLATFORMS

# Global instance
course_validator = CourseValidator()
