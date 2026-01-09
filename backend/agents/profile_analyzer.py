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
                error_msg = result.get("message", "Unknown error")
                print(f"LLM returned error in profile analyzer: {error_msg}")
                # Only use fallback if API key is missing or invalid
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    return self._generate_fallback_analysis(profile)
                # For other errors, still try to return partial result
                raise ValueError(error_msg)
            
            # Validate that we got a proper result with reasoning
            if not isinstance(result, dict):
                raise ValueError("LLM returned invalid result format")
            
            # Ensure reasoning field exists
            if "reasoning" not in result or not result.get("reasoning"):
                print("Warning: LLM response missing 'reasoning' field, adding default")
                result["reasoning"] = "AI analysis completed successfully. Your skills have been normalized and categorized based on industry standards."
            
            print(f"Profile Analyzer: Successfully generated analysis")
            return result
        except Exception as e:
            # If LLM fails completely, return fallback
            print(f"LLM service error in profile analyzer: {str(e)}")
            import traceback
            print(traceback.format_exc())
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
        
        # Generate a more detailed reasoning
        total_normalized = sum(len(v) for v in normalized.values())
        reasoning = f"""This analysis was generated using basic keyword matching (AI service temporarily unavailable).

Profile Summary:
- Experience Level: {experience_level}
- Total Skills Provided: {len(skills)}
- Skills Categorized: {total_normalized}

Skill Categories:
- Programming Languages: {len(normalized['programming_languages'])} skills
- Frameworks: {len(normalized['frameworks'])} skills
- Tools: {len(normalized['tools'])} skills
- Databases: {len(normalized['databases'])} skills

Your identified strengths: {', '.join(skills[:5]) if skills else 'None specified'}

For a more detailed analysis with better skill normalization, categorization, and personalized insights, please ensure the AI service is properly configured with a valid API key."""
        
        return {
            "normalized_skills": normalized,
            "experience_level": experience_level,
            "skill_summary": f"Profile with {len(skills)} skills at {experience_level} level",
            "strengths": skills[:3] if skills else [],
            "reasoning": reasoning,
            "fallback": True
        }

profile_analyzer = ProfileAnalyzerAgent()
