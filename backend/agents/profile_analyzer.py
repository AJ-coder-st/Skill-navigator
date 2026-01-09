"""
Profile Analyzer Agent
Normalizes and analyzes student profiles
"""

from typing import Dict, Any, List
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class ProfileAnalyzerAgent:
    """Analyzes and normalizes student profiles"""
    
    SYSTEM_PROMPT = """You are an expert career counselor. Your task is to analyze student profiles and normalize their skills.

Normalize skills to standard names (e.g., "Python 3" -> "Python", "JS" -> "JavaScript").
Categorize skills into:
- Programming languages
- Frameworks/libraries
- Tools/platforms
- Databases
- Soft skills
- Domain knowledge

Be consistent with skill naming."""

    async def analyze(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and normalize student profile with fallback"""
        
        prompt = f"""Analyze the following student profile and normalize it.

Student Profile:
{{
    "degree": "{profile.get('degree', 'Not specified')}",
    "skills": {profile.get('skills', [])},
    "experience_level": "{profile.get('experience_level', 'beginner')}",
    "projects": {profile.get('projects', [])},
    "certifications": {profile.get('certifications', [])}
}}

Return a JSON object with normalized skills:
{{
    "normalized_skills": {{
        "programming_languages": ["Python", "JavaScript", ...],
        "frameworks": ["React", "Django", ...],
        "tools": ["Git", "Docker", ...],
        "databases": ["PostgreSQL", "MongoDB", ...],
        "soft_skills": ["Communication", "Problem-solving", ...],
        "domain_knowledge": ["Web Development", "Data Analysis", ...]
    }},
    "experience_level": "beginner" | "intermediate" | "advanced",
    "skill_summary": "Brief summary of student's skill profile",
    "strengths": ["strength1", "strength2", ...],
    "reasoning": "Explanation of normalization decisions"
}}"""

        try:
            result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
            
            # Check if LLM returned an error
            if isinstance(result, dict) and result.get("error"):
                # Return fallback analysis
                return self._generate_fallback_analysis(profile)
            
            return result
        except Exception as e:
            # If LLM fails completely, return fallback
            print(f"LLM service error in profile analyzer: {str(e)}")
            return self._generate_fallback_analysis(profile)
    
    def _generate_fallback_analysis(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback analysis when LLM is unavailable"""
        skills = profile.get('skills', [])
        experience_level = profile.get('experience_level', 'beginner')
        
        # Simple normalization without LLM
        normalized = {
            "programming_languages": [],
            "frameworks": [],
            "tools": [],
            "databases": [],
            "soft_skills": [],
            "domain_knowledge": []
        }
        
        # Basic categorization
        for skill in skills:
            skill_lower = skill.lower()
            if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin']):
                normalized["programming_languages"].append(skill)
            elif any(fw in skill_lower for fw in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node']):
                normalized["frameworks"].append(skill)
            elif any(db in skill_lower for db in ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle']):
                normalized["databases"].append(skill)
            elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'ci/cd']):
                normalized["tools"].append(skill)
            else:
                normalized["tools"].append(skill)
        
        return {
            "normalized_skills": normalized,
            "experience_level": experience_level,
            "skill_summary": f"Profile with {len(skills)} skills at {experience_level} level",
            "strengths": skills[:3] if skills else [],
            "reasoning": "Fallback analysis generated (LLM temporarily unavailable)",
            "fallback": True
        }

profile_analyzer = ProfileAnalyzerAgent()
