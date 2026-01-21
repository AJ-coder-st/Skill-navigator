"""
Evaluation Harness - Automated Accuracy Evaluation
Measures skill-gap precision, recall, roadmap alignment, and course relevance
"""

from typing import Dict, Any, List, Set

class EvaluationHarness:
    """Evaluates accuracy of skill-gap mapping and recommendations"""
    
    def calculate_skill_gap_precision_recall(
        self,
        recommended_skills: List[str],
        required_skills: List[str],
        user_current_skills: List[str]
    ) -> Dict[str, float]:
        """
        Calculate precision and recall for skill-gap recommendations
        
        Args:
            recommended_skills: Skills recommended to learn
            required_skills: Skills actually required for the role
            user_current_skills: Skills user already has
        
        Returns:
            {
                "precision": float,
                "recall": float,
                "f1_score": float,
                "true_positives": int,
                "false_positives": int,
                "false_negatives": int
            }
        """
        # Skills user needs (required but not current)
        needed_skills = set(required_skills) - set(user_current_skills)
        
        # Recommended skills that are actually needed (true positives)
        true_positives = len(set(recommended_skills) & needed_skills)
        
        # Recommended skills that are NOT needed (false positives)
        false_positives = len(set(recommended_skills) - needed_skills)
        
        # Needed skills that were NOT recommended (false negatives)
        false_negatives = len(needed_skills - set(recommended_skills))
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1_score": round(f1_score, 3),
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "total_required": len(required_skills),
            "total_recommended": len(recommended_skills),
            "skills_needed": len(needed_skills)
        }
    
    def calculate_roadmap_alignment_score(
        self,
        roadmap_skills: List[str],
        skill_gaps: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate how well roadmap aligns with identified skill gaps
        
        Args:
            roadmap_skills: Skills covered in the roadmap
            skill_gaps: Skill gap analysis result
        
        Returns:
            {
                "alignment_score": float,
                "missing_skills_covered": int,
                "total_missing_skills": int,
                "coverage_percentage": float
            }
        """
        missing_skills = [gap.get("skill", "") for gap in skill_gaps.get("missing_skills", [])]
        roadmap_skills_set = set(roadmap_skills)
        missing_skills_set = set(missing_skills)
        
        # How many missing skills are covered in roadmap
        covered_missing = len(roadmap_skills_set & missing_skills_set)
        total_missing = len(missing_skills_set)
        
        coverage_percentage = (covered_missing / total_missing * 100) if total_missing > 0 else 100.0
        
        # Alignment score (0-1)
        alignment_score = covered_missing / total_missing if total_missing > 0 else 1.0
        
        return {
            "alignment_score": round(alignment_score, 3),
            "missing_skills_covered": covered_missing,
            "total_missing_skills": total_missing,
            "coverage_percentage": round(coverage_percentage, 2)
        }
    
    def calculate_course_relevance_score(
        self,
        recommended_courses: List[Dict[str, Any]],
        target_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate relevance of course recommendations to target skills
        
        Args:
            recommended_courses: List of recommended courses
            target_skills: Skills that need to be learned
        
        Returns:
            {
                "relevance_score": float,
                "courses_per_skill": float,
                "skill_coverage": Dict[str, int]
            }
        """
        if not recommended_courses or not target_skills:
            return {
                "relevance_score": 0.0,
                "courses_per_skill": 0.0,
                "skill_coverage": {}
            }
        
        # Count how many courses target each skill
        skill_coverage = {skill: 0 for skill in target_skills}
        
        for course in recommended_courses:
            course_skill = course.get("skill", "").lower()
            for target_skill in target_skills:
                if target_skill.lower() in course_skill or course_skill in target_skill.lower():
                    skill_coverage[target_skill] += 1
        
        # Calculate relevance: how many skills have at least one course
        skills_with_courses = sum(1 for count in skill_coverage.values() if count > 0)
        relevance_score = skills_with_courses / len(target_skills) if target_skills else 0.0
        
        courses_per_skill = len(recommended_courses) / len(target_skills) if target_skills else 0.0
        
        return {
            "relevance_score": round(relevance_score, 3),
            "courses_per_skill": round(courses_per_skill, 2),
            "skill_coverage": skill_coverage,
            "skills_with_courses": skills_with_courses,
            "total_skills": len(target_skills)
        }
    
    def evaluate_skill_gap_analysis(
        self,
        skill_gap_result: Dict[str, Any],
        job_requirements: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive evaluation of skill gap analysis
        
        Args:
            skill_gap_result: Result from skill gap analyzer
            job_requirements: Original job requirements
            user_profile: User's current profile
        
        Returns:
            Complete evaluation summary
        """
        # Extract skills
        recommended_skills = [
            gap.get("skill", "") 
            for gap in skill_gap_result.get("missing_skills", [])
        ]
        required_skills = job_requirements.get("required_skills", [])
        user_skills = []
        if "normalized_skills" in user_profile:
            for skill_list in user_profile["normalized_skills"].values():
                user_skills.extend(skill_list)
        
        # Calculate metrics
        precision_recall = self.calculate_skill_gap_precision_recall(
            recommended_skills,
            required_skills,
            user_skills
        )
        
        roadmap_alignment = self.calculate_roadmap_alignment_score(
            recommended_skills,
            skill_gap_result
        )
        
        return {
            "skill_gap_precision": precision_recall["precision"],
            "skill_gap_recall": precision_recall["recall"],
            "skill_gap_f1": precision_recall["f1_score"],
            "roadmap_alignment_score": roadmap_alignment["alignment_score"],
            "detailed_metrics": {
                "precision_recall": precision_recall,
                "roadmap_alignment": roadmap_alignment
            },
            "evaluation_summary": self._format_evaluation_summary(
                precision_recall,
                roadmap_alignment
            )
        }
    
    def _format_evaluation_summary(
        self,
        precision_recall: Dict[str, Any],
        roadmap_alignment: Dict[str, Any]
    ) -> str:
        """Format evaluation results as summary text"""
        precision = precision_recall["precision"]
        recall = precision_recall["recall"]
        alignment = roadmap_alignment["alignment_score"]
        
        # Determine quality level
        if precision >= 0.8 and recall >= 0.8:
            quality = "High"
        elif precision >= 0.6 and recall >= 0.6:
            quality = "Medium"
        else:
            quality = "Low"
        
        return (
            f"Evaluation Summary:\n"
            f"Skill-Gap Precision: {precision:.2f}\n"
            f"Skill-Gap Recall: {recall:.2f}\n"
            f"Roadmap Alignment Score: {quality}"
        )

# Global instance
evaluation_harness = EvaluationHarness()
