"""
Reflection Agent
Reflects on progress and updates recommendations
"""

from typing import Dict, Any, List
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class ReflectionAgent:
    """Reflects on student progress and updates roadmap"""
    
    SYSTEM_PROMPT = """You are an expert learning coach. Your task is to analyze student progress and update their learning roadmap.

Consider:
1. What has been completed
2. Confidence levels in different skills
3. Areas needing more practice
4. Adjust timeline if needed
5. Provide encouragement and next steps"""

    async def reflect(self, original_roadmap: Dict[str, Any], progress: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on progress and generate updated recommendations"""
        
        prompt = f"""Analyze student progress and update the learning roadmap.

Original Roadmap:
{{
    "total_weeks": {original_roadmap.get('total_weeks', 8)},
    "weeks": {original_roadmap.get('weeks', [])}
}}

Student Progress:
{{
    "completed_milestones": {progress.get('completed_milestones', [])},
    "current_week": {progress.get('current_week', 1)},
    "skill_confidence": {progress.get('skill_confidence', {})},
    "completed_practices": {progress.get('completed_practices', [])},
    "challenges_faced": {progress.get('challenges_faced', [])}
}}

Return a JSON object with updated recommendations:
{{
    "progress_summary": "Overall progress assessment",
    "strengths_identified": ["strength1", "strength2"],
    "areas_needing_attention": [
        {{
            "area": "skill or topic",
            "reason": "Why this needs attention",
            "recommendation": "What to do"
        }}
    ],
    "updated_roadmap": {{
        "adjustments": ["adjustment1", "adjustment2"],
        "next_priorities": ["priority1", "priority2"],
        "timeline_changes": "Any changes to timeline"
    }},
    "encouragement": "Motivational message",
    "reasoning": "Explanation of the reflection and recommendations"
}}"""

        result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
        return result

reflection_agent = ReflectionAgent()
