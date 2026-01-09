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
        
        # Debug: Print input data
        print(f"Skill Gap Analysis - Input Debug:")
        print(f"  Job Skills - Role: {job_skills.get('role', 'Unknown')}")
        print(f"  Job Skills - Required: {job_skills.get('required_skills', [])}")
        print(f"  Job Skills - Preferred: {job_skills.get('preferred_skills', [])}")
        print(f"  Student Profile - Normalized Skills: {student_profile.get('normalized_skills', {})}")
        print(f"  Student Profile - Experience: {student_profile.get('experience_level', 'beginner')}")
        
        # Check if we have required skills to analyze
        required_skills = job_skills.get('required_skills', [])
        if not required_skills or len(required_skills) == 0:
            print("Warning: No required skills found in job_skills, using fallback analysis")
            return self.fallback_analyze(job_skills, student_profile)
        
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

        try:
            result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
            
            # Validate result
            if not result or not isinstance(result, dict):
                print("Warning: LLM returned invalid result, using fallback")
                return self.fallback_analyze(job_skills, student_profile)
            
            # Check if result has error
            if result.get("error"):
                error_msg = result.get("message", "Unknown error")
                print(f"LLM returned error in skill gap analyzer: {error_msg}")
                # Only use fallback if API key is missing or invalid
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    return self.fallback_analyze(job_skills, student_profile)
                # For other errors, still try to return partial result
                raise ValueError(error_msg)
            
            # Check if result has skills
            missing = result.get("missing_skills", [])
            partial = result.get("partial_skills", [])
            strong = result.get("strong_skills", [])
            
            if (not missing or len(missing) == 0) and (not partial or len(partial) == 0) and (not strong or len(strong) == 0):
                print("Warning: LLM returned empty skills, using fallback")
                return self.fallback_analyze(job_skills, student_profile)
            
            # Ensure reasoning field exists
            if "reasoning" not in result or not result.get("reasoning"):
                print("Warning: LLM response missing 'reasoning' field, adding default")
                result["reasoning"] = f"AI analysis completed successfully. Identified {len(missing)} missing skills, {len(partial)} skills needing improvement, and {len(strong)} strong skills. This analysis helps prioritize your learning path."
            
            print(f"LLM analysis successful: missing={len(missing)}, partial={len(partial)}, strong={len(strong)}")
            return result
            
        except Exception as e:
            # Fallback to keyword-based analysis if LLM fails
            print(f"LLM error in skill gap analysis: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self.fallback_analyze(job_skills, student_profile)
    
    def fallback_analyze(self, job_skills: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback keyword-based skill gap analysis when LLM is unavailable"""
        
        print("Using fallback keyword-based analysis")
        
        required_skills = job_skills.get('required_skills', [])
        preferred_skills = job_skills.get('preferred_skills', [])
        
        if not required_skills:
            print("Warning: No required_skills found in job_skills")
            # Try to extract from other fields
            if 'skills' in job_skills:
                required_skills = job_skills['skills'] if isinstance(job_skills['skills'], list) else [job_skills['skills']]
        
        print(f"Fallback: Analyzing {len(required_skills)} required skills")
        
        # Get student skills from normalized_skills
        student_skills_dict = student_profile.get('normalized_skills', {})
        student_skills = []
        
        if isinstance(student_skills_dict, dict):
            for category, skills in student_skills_dict.items():
                if isinstance(skills, list):
                    student_skills.extend([str(s).lower() for s in skills if s])
                elif isinstance(skills, str) and skills:
                    student_skills.append(skills.lower())
        elif isinstance(student_skills_dict, list):
            student_skills = [str(s).lower() for s in student_skills_dict if s]
        
        # Also check if skills are in the profile directly
        if 'skills' in student_profile:
            profile_skills = student_profile['skills']
            if isinstance(profile_skills, list):
                student_skills.extend([str(s).lower() for s in profile_skills if s])
            elif isinstance(profile_skills, str):
                student_skills.extend([s.strip().lower() for s in profile_skills.split(',') if s.strip()])
        
        # Remove duplicates
        student_skills = list(set(student_skills))
        print(f"Fallback: Found {len(student_skills)} student skills: {student_skills[:10]}...")
        
        # Categorize skills
        missing_skills = []
        partial_skills = []
        strong_skills = []
        
        for skill in required_skills:
            if not skill:
                continue
                
            skill_str = str(skill).strip()
            skill_lower = skill_str.lower()
            
            # Check for exact match
            if skill_lower in student_skills:
                strong_skills.append({
                    "skill": skill_str,
                    "confidence": "high",
                    "suggestion": f"You have {skill_str} - leverage this in your application"
                })
            else:
                # Check for partial match (keyword matching)
                found_partial = False
                for student_skill in student_skills:
                    # More flexible matching
                    if (skill_lower in student_skill or 
                        student_skill in skill_lower or
                        any(word in student_skill for word in skill_lower.split() if len(word) > 3)):
                        partial_skills.append({
                            "skill": skill_str,
                            "current_level": f"You have related knowledge in {student_skill}",
                            "target_level": f"Master {skill_str}",
                            "gap_analysis": f"Build on your {student_skill} knowledge to master {skill_str}",
                            "estimated_time_to_improve": "2-4 weeks"
                        })
                        found_partial = True
                        break
                
                if not found_partial:
                    missing_skills.append({
                        "skill": skill_str,
                        "category": "unknown",
                        "priority": "high",
                        "importance": f"{skill_str} is required for this role",
                        "estimated_time_to_learn": "4-8 weeks"
                    })
        
        print(f"Fallback result: missing={len(missing_skills)}, partial={len(partial_skills)}, strong={len(strong_skills)}")
        
        # Generate a more detailed reasoning
        total_required = len(required_skills)
        match_percentage = (len(strong_skills) / total_required * 100) if total_required > 0 else 0
        
        reasoning = f"""This analysis was generated using keyword-based matching (AI service temporarily unavailable).

Analysis Summary:
- Total Required Skills Analyzed: {total_required}
- Skills You Have: {len(strong_skills)} ({match_percentage:.1f}% match)
- Skills Needing Improvement: {len(partial_skills)}
- Missing Skills: {len(missing_skills)}

Detailed Breakdown:
• Strong Skills ({len(strong_skills)}): You have these skills and can confidently highlight them in your application.
• Partial Skills ({len(partial_skills)}): You have related knowledge but need to strengthen these areas.
• Missing Skills ({len(missing_skills)}): These are critical gaps you should prioritize learning.

Recommendations:
1. Focus on learning the {len(missing_skills)} missing skills first, as they are required for the role
2. Improve your {len(partial_skills)} partial skills through practice and projects
3. Leverage your {len(strong_skills)} strong skills to demonstrate competency

For a more detailed AI-powered analysis with personalized learning recommendations, time estimates, and strategic insights, please ensure the AI service is properly configured with a valid API key."""
        
        return {
            "missing_skills": missing_skills,
            "partial_skills": partial_skills,
            "strong_skills": strong_skills,
            "overall_assessment": f"You have {len(strong_skills)} strong skills, {len(partial_skills)} partial skills, and {len(missing_skills)} missing skills",
            "reasoning": reasoning,
            "fallback": True
        }

skill_gap_analyzer = SkillGapAnalyzerAgent()
