"""
Practice Generator Agent
Generates tailored practice tasks, coding challenges, and interview prep
"""

from typing import Dict, Any, List
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class PracticeGeneratorAgent:
    """Generates practice tasks, coding challenges, and interview prep materials"""
    
    SYSTEM_PROMPT = """You are an expert coding instructor and interview coach. Your task is to generate realistic practice materials.

Generate:
1. Coding challenges appropriate for the skill level
2. Behavioral interview questions relevant to the role
3. Mini-project ideas that demonstrate skills
4. All tasks should be achievable and educational"""

    async def generate(self, roadmap: Dict[str, Any], role: str, skill_gaps: Dict[str, Any]) -> Dict[str, Any]:
        """Generate practice materials"""
        
        prompt = f"""Generate practice materials for a student preparing for this role: {role}

Current Roadmap:
{{
    "weeks": {roadmap.get('weeks', [])[:3]}  # First 3 weeks
}}

Skill Gaps:
{{
    "missing_skills": {skill_gaps.get('missing_skills', [])[:5]},
    "partial_skills": {skill_gaps.get('partial_skills', [])[:3]}
}}

Return a JSON object with practice materials:
{{
    "coding_challenges": [
        {{
            "title": "Challenge name",
            "difficulty": "beginner" | "intermediate" | "advanced",
            "skill_focus": "skill_name",
            "description": "Problem description",
            "requirements": ["requirement1", "requirement2"],
            "hints": ["hint1", "hint2"],
            "estimated_time": "X hours"
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "Interview question",
            "skill_focus": "soft_skill or role-specific",
            "guidance": "What interviewers are looking for",
            "sample_answer_structure": "How to structure the answer"
        }}
    ],
    "mini_projects": [
        {{
            "title": "Project name",
            "description": "Project description",
            "skills_demonstrated": ["skill1", "skill2"],
            "scope": "What to build",
            "deliverables": ["deliverable1", "deliverable2"],
            "estimated_time": "X weeks",
            "difficulty": "beginner" | "intermediate" | "advanced"
        }}
    ],
    "reasoning": "Explanation of why these practice materials were chosen"
}}"""

        result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
        return result

practice_generator = PracticeGeneratorAgent()
