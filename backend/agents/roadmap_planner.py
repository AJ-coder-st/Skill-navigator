"""
Roadmap Planner Agent
Generates realistic learning roadmaps
"""

from typing import Dict, Any, List
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service
from core.rag_service import rag_service

class RoadmapPlannerAgent:
    """Generates realistic, milestone-based learning roadmaps"""
    
    SYSTEM_PROMPT = """You are an expert learning path designer. Your task is to create realistic, milestone-based learning roadmaps.

Key principles:
1. Be realistic about learning timelines (no "learn ML in 1 week")
2. Build skills progressively (foundations first)
3. Include milestones and checkpoints
4. Consider dependencies between skills
5. Allocate time for practice, not just theory
6. Typical timeline: 6-8 weeks for significant skill development"""

    async def generate(self, skill_gaps: Dict[str, Any], time_weeks: int = 8) -> Dict[str, Any]:
        """Generate learning roadmap"""
        
        # Retrieve relevant courses for missing skills
        missing_skills = [gap["skill"] for gap in skill_gaps.get("missing_skills", [])]
        course_recommendations = {}
        
        for skill in missing_skills[:10]:  # Limit to avoid too many API calls
            courses = await rag_service.retrieve_courses(skill, skill_gaps.get("role", ""))
            course_recommendations[skill] = courses[:3]  # Top 3 per skill
        
        prompt = f"""Create a realistic {time_weeks}-week learning roadmap based on the skill gap analysis.

Skill Gaps:
{{
    "missing_skills": {skill_gaps.get('missing_skills', [])},
    "partial_skills": {skill_gaps.get('partial_skills', [])},
    "overall_assessment": "{skill_gaps.get('overall_assessment', '')}"
}}

Available Course Resources:
{self._format_courses(course_recommendations)}

Return a JSON object with a week-by-week roadmap:
{{
    "total_weeks": {time_weeks},
    "weeks": [
        {{
            "week_number": 1,
            "focus_skills": ["skill1", "skill2"],
            "milestones": [
                {{
                    "title": "Milestone name",
                    "description": "What to achieve",
                    "skills_covered": ["skill1"],
                    "resources": ["resource_name or URL"],
                    "estimated_hours": 10
                }}
            ],
            "learning_objectives": ["objective1", "objective2"],
            "practice_tasks": ["task1", "task2"],
            "checkpoint": "How to verify progress"
        }}
    ],
    "reasoning": "Explanation of the roadmap structure and why skills are ordered this way"
}}"""

        result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
        return result
    
    def _format_courses(self, course_recommendations: Dict[str, List]) -> str:
        """Format course recommendations for prompt"""
        formatted = ""
        for skill, courses in course_recommendations.items():
            formatted += f"\n{skill}:\n"
            for course in courses:
                formatted += f"  - {course.get('resource_name', 'Unknown')} ({course.get('provider', 'Unknown')})\n"
        return formatted

roadmap_planner = RoadmapPlannerAgent()
