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
from core.course_validator import course_validator
from core.citation_formatter import citation_formatter
from core.safety_filters import safety_filters

class RoadmapPlannerAgent:
    """Generates realistic, milestone-based learning roadmaps"""
    
    SYSTEM_PROMPT = """You are an expert learning path designer. Your task is to create realistic, milestone-based learning roadmaps.

Key principles:
1. Be realistic about learning timelines (no "learn ML in 1 week")
2. Build skills progressively (foundations first)
3. Include milestones and checkpoints
4. Consider dependencies between skills
5. Allocate time for practice, not just theory
6. Typical timeline: 6-8 weeks for significant skill development
7. NEVER claim guaranteed jobs, salaries, or outcomes
8. ONLY recommend courses that are provided in the available resources list
9. Do NOT invent or hallucinate course names, providers, or URLs"""

    async def generate(self, skill_gaps: Dict[str, Any], time_weeks: int = 8) -> Dict[str, Any]:
        """Generate learning roadmap"""
        
        # Retrieve relevant courses for missing skills
        missing_skills = [gap["skill"] for gap in skill_gaps.get("missing_skills", [])]
        course_recommendations = {}
        
        for skill in missing_skills[:10]:  # Limit to avoid too many API calls
            courses = await rag_service.retrieve_courses(skill, skill_gaps.get("role", ""))
            # Validate courses to prevent hallucination
            validated_courses = await course_validator.filter_valid_courses(courses)
            course_recommendations[skill] = validated_courses[:3]  # Top 3 per skill
        
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
                    "resources_cited": [
                        {{
                            "course_name": "Course Name",
                            "platform": "Platform",
                            "url": "https://example.com",
                            "citation": "Platform – Course Name (URL)"
                        }}
                    ],
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
        
        # Add citations to roadmap
        result = citation_formatter.format_roadmap_citations(result, course_recommendations)
        
        # Apply safety filters
        result = safety_filters.apply_safety_wrapper(
            result, 
            text_fields=["reasoning", "overall_assessment"]
        )
        
        # Add course validation status
        result["course_validation"] = {
            "all_courses_validated": True,
            "total_courses": sum(len(courses) for courses in course_recommendations.values()),
            "verified_platforms_only": True
        }
        
        return result
    
    def _format_courses(self, course_recommendations: Dict[str, List]) -> str:
        """Format course recommendations for prompt with citations"""
        formatted = ""
        for skill, courses in course_recommendations.items():
            formatted += f"\n{skill}:\n"
            for course in courses:
                citation = citation_formatter.format_course_citation(course)
                formatted += f"  - {citation}\n"
        return formatted

roadmap_planner = RoadmapPlannerAgent()
