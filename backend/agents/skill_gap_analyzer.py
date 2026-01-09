"""
Skill Gap Analyzer Agent
Identifies gaps between job requirements and student profile
"""

from typing import Dict, Any, List
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class SkillGapAnalyzerAgent:
    """Analyzes skill gaps between job requirements and student profile"""
    
    SYSTEM_PROMPT = """You are an expert career advisor. Your task is to identify skill gaps between job requirements and a student's current profile.

For each required skill, determine:
- Missing: Student doesn't have this skill
- Partial: Student has related knowledge but needs improvement
- Strong: Student has this skill

Provide clear explanations for why each skill matters for the role and what the gap means."""

    async def analyze(self, job_skills: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps"""
        
        prompt = f"""Analyze the skill gaps between the job requirements and student profile.

Job Requirements:
{{
    "role": "{job_skills.get('role', 'Unknown')}",
    "required_skills": {job_skills.get('required_skills', [])},
    "preferred_skills": {job_skills.get('preferred_skills', [])},
    "experience_level": "{job_skills.get('experience_level', 'mid')}"
}}

Student Profile:
{{
    "normalized_skills": {student_profile.get('normalized_skills', {})},
    "experience_level": "{student_profile.get('experience_level', 'beginner')}"
}}

Return a JSON object with skill gap analysis:
{{
    "missing_skills": [
        {{
            "skill": "skill_name",
            "category": "programming_language" | "framework" | "tool" | "database" | "soft_skill",
            "priority": "high" | "medium" | "low",
            "importance": "Why this skill is critical for the role",
            "estimated_time_to_learn": "X weeks"
        }}
    ],
    "partial_skills": [
        {{
            "skill": "skill_name",
            "current_level": "description",
            "target_level": "description",
            "gap_analysis": "What needs improvement",
            "estimated_time_to_improve": "X weeks"
        }}
    ],
    "strong_skills": [
        {{
            "skill": "skill_name",
            "confidence": "high" | "medium",
            "suggestion": "How to leverage this strength"
        }}
    ],
    "overall_assessment": "Overall assessment of readiness",
    "reasoning": "Detailed explanation of the analysis"
}}"""

        result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
        return result

skill_gap_analyzer = SkillGapAnalyzerAgent()
