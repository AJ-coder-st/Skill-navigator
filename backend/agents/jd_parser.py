"""
JD Parser Agent
Extracts structured skill requirements from job descriptions
"""

from typing import Dict, Any, List
import sys
# Import appropriate LLM service based on Python version
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service
from core.rag_service import rag_service

class JDParserAgent:
    """Parses unstructured job descriptions into structured skill requirements"""
    
    SYSTEM_PROMPT = """You are an expert job description analyzer. Your task is to extract structured information from job descriptions.

Extract the following:
1. Required technical skills (programming languages, tools, frameworks)
2. Preferred/optional skills
3. Soft skills
4. Experience level (entry, mid, senior)
5. Education requirements
6. Key responsibilities

Be precise and realistic. Only extract skills that are explicitly mentioned or clearly implied."""

    async def parse(self, job_description: str) -> Dict[str, Any]:
        """Parse job description into structured format with fallback"""
        
        # Retrieve similar job descriptions for context
        # Extract role name first (simple heuristic)
        role_keywords = job_description[:200].lower()
        similar_jds = await rag_service.retrieve_job_samples(role_keywords)
        
        # Build context from similar JDs
        context = ""
        if similar_jds:
            context = "\n\nSimilar job descriptions for reference:\n"
            for jd in similar_jds[:3]:
                context += f"- Role: {jd.get('role', 'Unknown')}\n"
                context += f"  Skills: {', '.join(jd.get('skills', []))}\n"
        
        prompt = f"""Analyze the following job description and extract structured information.

Job Description:
{job_description}
{context}

Return a JSON object with the following structure:
{{
    "role": "Job title/role name",
    "required_skills": ["skill1", "skill2", ...],
    "preferred_skills": ["skill1", "skill2", ...],
    "soft_skills": ["skill1", "skill2", ...],
    "experience_level": "entry" | "mid" | "senior",
    "education_requirements": "description",
    "key_responsibilities": ["responsibility1", "responsibility2", ...],
    "reasoning": "Brief explanation of why these skills were extracted"
}}"""

        try:
            result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
            
            # Check if LLM returned an error
            if isinstance(result, dict) and result.get("error"):
                # Return fallback analysis
                return self._generate_fallback_parse(job_description, similar_jds)
            
            return result
        except Exception as e:
            # If LLM fails completely, return fallback
            print(f"LLM service error in JD parser: {str(e)}")
            return self._generate_fallback_parse(job_description, similar_jds)
    
    def _generate_fallback_parse(self, job_description: str, similar_jds: List[Dict]) -> Dict[str, Any]:
        """Generate fallback parsing when LLM is unavailable"""
        # Extract role from first line or title
        role = "Software Developer"
        if "Job Title:" in job_description or "Title:" in job_description:
            lines = job_description.split('\n')
            for line in lines:
                if "Title:" in line or "Job Title:" in line:
                    role = line.split(':')[1].strip() if ':' in line else line.strip()
                    break
        
        # Extract skills using keyword matching
        jd_lower = job_description.lower()
        common_skills = {
            "SQL", "Python", "JavaScript", "Java", "React", "Node.js", "AWS", "Docker",
            "Git", "MongoDB", "PostgreSQL", "Excel", "Tableau", "Machine Learning",
            "Data Analysis", "Statistics", "REST APIs", "TypeScript", "HTML", "CSS"
        }
        
        found_skills = [skill for skill in common_skills if skill.lower() in jd_lower]
        
        # Determine experience level
        experience_level = "mid"
        if any(word in jd_lower for word in ["entry", "junior", "intern", "graduate"]):
            experience_level = "entry"
        elif any(word in jd_lower for word in ["senior", "lead", "principal", "architect"]):
            experience_level = "senior"
        
        return {
            "role": role,
            "required_skills": found_skills[:10],
            "preferred_skills": [],
            "soft_skills": ["Communication", "Problem-solving"],
            "experience_level": experience_level,
            "education_requirements": "Bachelor's degree or equivalent",
            "key_responsibilities": ["See job description for details"],
            "reasoning": "Fallback analysis generated (LLM temporarily unavailable)",
            "fallback": True
        }

jd_parser = JDParserAgent()
