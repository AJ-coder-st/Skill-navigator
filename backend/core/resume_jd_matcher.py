"""
Resume-JD Matcher Service
Compares candidate resume profile with job requirements
Implements fair and realistic scoring that rewards partial matches
"""

from typing import Dict, Any, List, Tuple
import sys
import re
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class ResumeJDMatcher:
    """Matches resume profile against job description requirements with fair scoring"""
    
    SYSTEM_PROMPT = """You are an expert Resume-Job Matching and Scoring Engine. Your responsibility is to compute a FAIR and REALISTIC match score.

SCORING PRINCIPLES:
1. Partial matches MUST be rewarded (Docker → Cloud, MERN → Full Stack)
2. Experience requirements are SOFT constraints (apply penalty, not rejection)
3. Do NOT penalize students, interns, or project-based learning
4. Never return 0 unless ABSOLUTELY no relevance exists

WEIGHTED SCORING MODEL:
- Core Technical Skills: 40%
- Project & Practical Experience: 25%
- Tools & Ecosystem: 15%
- Experience Alignment: 10%
- Soft Skills & Collaboration: 10%

EXPERIENCE EQUIVALENCE:
- 2 major full-stack projects = 1 year experience
- Internship = professional exposure
- Production delivery = strong signal

Return JSON with match_percentage (0-100), match_level, matched_skills, partial_matches, missing_skills, and scoring_explanation."""

    async def match(self, candidate_profile: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Match candidate profile against job requirements with fair scoring"""
        
        prompt = f"""Compare the following candidate resume profile with job requirements and generate a FAIR match analysis.

CRITICAL RULES:
- NEVER return 0% unless ABSOLUTELY no relevance exists
- Reward partial matches (Docker → Cloud readiness, MERN → Full Stack)
- Do NOT penalize students, interns, or project-based learning
- Apply SOFT constraints for experience (penalty, not rejection)

Candidate Profile:
{{
    "name": "{candidate_profile.get('personal_info', {}).get('name', 'N/A')}",
    "education": {candidate_profile.get('education', [])},
    "experience_years": "{candidate_profile.get('experience_years', '0')}",
    "skills": {candidate_profile.get('skills', {})},
    "projects": {candidate_profile.get('projects', [])},
    "certifications": {candidate_profile.get('certifications', [])},
    "experience": {candidate_profile.get('experience', [])}
}}

Job Requirements:
{{
    "role": "{job_requirements.get('role', 'N/A')}",
    "core_skills": {job_requirements.get('required_skills', [])},
    "preferred_skills": {job_requirements.get('preferred_skills', [])},
    "experience_required": "{job_requirements.get('experience_level', 'mid')}",
    "soft_skills": {job_requirements.get('soft_skills', [])}
}}

Calculate match using WEIGHTED SCORING MODEL (Total: 100):
- Core Technical Skills: 40% (exact + partial matches)
- Project & Practical Experience: 25% (2 major projects = 1 year experience)
- Tools & Ecosystem: 15% (Git, Docker, CI/CD, Cloud)
- Experience Alignment: 10% (apply penalty for gap, don't reject)
- Soft Skills & Collaboration: 10% (teamwork, communication)

EXPERIENCE EQUIVALENCE:
- 2 major full-stack projects = 1 year experience
- Internship = professional exposure
- Production deployment = strong signal

Return JSON ONLY with this exact structure:
{{
    "match_percentage": number (0-100, NEVER 0 unless absolutely no relevance),
    "match_level": "Low" | "Moderate" | "Good" | "Strong",
    "matched_skills": ["skill1", "skill2"],
    "partial_matches": ["skill1 (Docker shows Cloud readiness)", "skill2 (MERN → Full Stack)"],
    "missing_skills": ["skill1", "skill2"],
    "scoring_explanation": "Clear human-readable justification of the score and level"
}}"""

        try:
            result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
            
            # Check if LLM returned an error
            if isinstance(result, dict) and result.get("error"):
                error_msg = result.get("message", "Unknown error")
                print(f"LLM returned error in resume-JD matcher: {error_msg}")
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    return self._generate_fallback_match(candidate_profile, job_requirements)
                raise ValueError(error_msg)
            
            # Validate result structure
            if not isinstance(result, dict):
                raise ValueError("LLM returned invalid result format")
            
            # Validate and normalize result structure
            match_percentage = result.get("match_percentage", 0)
            if isinstance(match_percentage, str):
                try:
                    match_percentage = int(float(match_percentage))
                except:
                    match_percentage = 0
            
            # Ensure match_percentage is never 0 unless absolutely no relevance
            matched_skills = result.get("matched_skills", [])
            partial_matches = result.get("partial_matches", [])
            if match_percentage == 0 and (matched_skills or partial_matches):
                # Recalculate minimum score if there are any matches
                match_percentage = max(15, len(matched_skills) * 10 + len(partial_matches) * 5)
            
            # Ensure match_level exists
            if "match_level" not in result:
                if match_percentage >= 80:
                    match_level = "Strong"
                elif match_percentage >= 60:
                    match_level = "Good"
                elif match_percentage >= 40:
                    match_level = "Moderate"
                else:
                    match_level = "Low"
                result["match_level"] = match_level
            
            # Ensure scoring_explanation exists
            if "scoring_explanation" not in result or not result.get("scoring_explanation"):
                result["scoring_explanation"] = f"Match score of {match_percentage}% based on {len(matched_skills)} exact skill matches and {len(partial_matches)} partial matches."
            
            result["match_percentage"] = match_percentage
            result.setdefault("matched_skills", [])
            result.setdefault("partial_matches", [])
            result.setdefault("missing_skills", [])
            
            print(f"Resume-JD Matcher: Successfully generated match analysis - {match_percentage}% ({result['match_level']})")
            return result
        except Exception as e:
            print(f"LLM service error in resume-JD matcher: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self._generate_fallback_match(candidate_profile, job_requirements)
    
    def _generate_fallback_match(self, candidate_profile: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback matching with fair scoring when LLM is unavailable"""
        
        # Extract candidate skills
        candidate_skills_dict = candidate_profile.get('skills', {})
        candidate_skills_list = []
        if isinstance(candidate_skills_dict, dict):
            candidate_skills_list.extend(candidate_skills_dict.get('technical_skills', []))
            candidate_skills_list.extend(candidate_skills_dict.get('programming_languages', []))
            candidate_skills_list.extend(candidate_skills_dict.get('tools_frameworks', []))
            candidate_skills_list.extend(candidate_skills_dict.get('soft_skills', []))
        elif isinstance(candidate_skills_dict, list):
            candidate_skills_list = candidate_skills_dict
        
        # Normalize to lowercase for comparison
        candidate_skills_lower = [s.lower().strip() for s in candidate_skills_list]
        
        # Extract job requirements
        required_skills = job_requirements.get('required_skills', [])
        preferred_skills = job_requirements.get('preferred_skills', [])
        
        # Define skill categories and partial match mappings
        skill_categories = {
            "frontend": ["react", "vue", "angular", "javascript", "typescript", "html", "css"],
            "backend": ["node", "python", "java", "django", "flask", "express", "fastapi"],
            "database": ["sql", "mysql", "postgresql", "mongodb", "redis"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "cloud"],
            "devops": ["docker", "kubernetes", "ci/cd", "jenkins", "git"],
            "fullstack": ["mern", "mean", "react", "node", "full stack", "full-stack"]
        }
        
        # Match skills with partial matching
        matched_skills = []
        partial_matches = []
        missing_skills = []
        
        for skill in required_skills:
            skill_lower = skill.lower().strip()
            matched = False
            
            # Exact match
            if skill_lower in candidate_skills_lower:
                matched_skills.append(skill)
                matched = True
            else:
                # Check for partial matches
                for candidate_skill in candidate_skills_lower:
                    if skill_lower in candidate_skill or candidate_skill in skill_lower:
                        partial_matches.append(f"{skill} (related: {candidate_skill})")
                        matched = True
                        break
                    
                    # Check category-based partial matches
                    for category, keywords in skill_categories.items():
                        if skill_lower in keywords and any(kw in candidate_skill for kw in keywords):
                            partial_matches.append(f"{skill} (category match: {category})")
                            matched = True
                            break
                    if matched:
                        break
            
            if not matched:
                missing_skills.append(skill)
        
        # Calculate experience equivalent (2 major projects = 1 year)
        experience_years_str = candidate_profile.get('experience_years', '0')
        try:
            exp_years = float(re.sub(r'[^0-9.]', '', str(experience_years_str)))
        except:
            exp_years = 0
        
        projects = candidate_profile.get('projects', [])
        project_count = len(projects) if isinstance(projects, list) else 0
        project_equivalent_years = project_count / 2.0  # 2 projects = 1 year
        
        # Check for internships
        experience = candidate_profile.get('experience', [])
        has_internship = any(
            'intern' in str(exp).lower() or 'internship' in str(exp).lower() 
            for exp in experience
        ) if isinstance(experience, list) else False
        
        total_equivalent_years = exp_years + project_equivalent_years + (0.5 if has_internship else 0)
        
        # WEIGHTED SCORING MODEL
        # Core Technical Skills: 40%
        required_count = len(required_skills) if required_skills else 1
        exact_match_score = (len(matched_skills) / required_count) * 40
        partial_match_score = (len(partial_matches) / required_count) * 20  # Partial = 50% credit
        core_skills_score = min(40, exact_match_score + partial_match_score)
        
        # Project & Practical Experience: 25%
        has_projects = project_count > 0
        has_production = any(
            'production' in str(proj).lower() or 'deploy' in str(proj).lower()
            for proj in projects
        ) if isinstance(projects, list) else False
        project_score = min(25, (project_count * 5) + (10 if has_production else 0))
        
        # Tools & Ecosystem: 15%
        tools_required = [s for s in required_skills if any(tool in s.lower() for tool in ['git', 'docker', 'ci/cd', 'cloud', 'aws', 'azure'])]
        tools_matched = sum(1 for tool in tools_required if any(tool.lower() in cs for cs in candidate_skills_lower))
        tools_score = (tools_matched / len(tools_required) * 15) if tools_required else 0
        
        # Experience Alignment: 10% (soft constraint - apply penalty, don't reject)
        experience_level = job_requirements.get('experience_level', 'mid').lower()
        if experience_level == 'entry':
            exp_target = 1
        elif experience_level == 'senior':
            exp_target = 5
        else:  # mid
            exp_target = 3
        
        if total_equivalent_years >= exp_target:
            exp_score = 10
        elif total_equivalent_years >= exp_target * 0.5:
            exp_score = 7  # Small penalty
        elif total_equivalent_years > 0:
            exp_score = 5  # Medium penalty
        else:
            exp_score = 2  # Large penalty but not zero
        
        # Soft Skills & Collaboration: 10%
        soft_skills = job_requirements.get('soft_skills', [])
        candidate_soft = candidate_skills_dict.get('soft_skills', []) if isinstance(candidate_skills_dict, dict) else []
        soft_matched = sum(1 for s in soft_skills if any(s.lower() in cs.lower() for cs in candidate_soft))
        soft_score = (soft_matched / len(soft_skills) * 10) if soft_skills else 5
        
        # Calculate total score (NEVER 0 unless absolutely no relevance)
        total_score = core_skills_score + project_score + tools_score + exp_score + soft_score
        match_percentage = max(5, min(100, int(total_score)))  # Minimum 5% if any relevance exists
        
        # Determine match level
        if match_percentage >= 80:
            match_level = "Strong"
        elif match_percentage >= 60:
            match_level = "Good"
        elif match_percentage >= 40:
            match_level = "Moderate"
        else:
            match_level = "Low"
        
        # Generate scoring explanation
        explanation_parts = []
        explanation_parts.append(f"Core Technical Skills: {len(matched_skills)} exact matches, {len(partial_matches)} partial matches ({core_skills_score:.1f}/40)")
        if project_count > 0:
            explanation_parts.append(f"Project Experience: {project_count} projects = {project_equivalent_years:.1f} years equivalent ({project_score:.1f}/25)")
        if has_internship:
            explanation_parts.append(f"Internship experience counts as professional exposure (+0.5 years)")
        explanation_parts.append(f"Tools & Ecosystem: {tools_matched}/{len(tools_required) if tools_required else 0} matched ({tools_score:.1f}/15)")
        explanation_parts.append(f"Experience Alignment: {total_equivalent_years:.1f} equivalent years vs {exp_target} required ({exp_score}/10)")
        if soft_skills:
            explanation_parts.append(f"Soft Skills: {soft_matched}/{len(soft_skills)} matched ({soft_score:.1f}/10)")
        explanation_parts.append(f"Total Score: {match_percentage}% ({match_level} match)")
        
        scoring_explanation = ". ".join(explanation_parts) + "."
        
        return {
            "match_percentage": match_percentage,
            "match_level": match_level,
            "matched_skills": matched_skills,
            "partial_matches": partial_matches,
            "missing_skills": missing_skills,
            "scoring_explanation": scoring_explanation,
            "fallback": True
        }

resume_jd_matcher = ResumeJDMatcher()
