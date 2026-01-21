"""
User Feedback System - Collects and stores user satisfaction data
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from core.database import get_database

class FeedbackSystem:
    """Manages user feedback collection and storage"""
    
    async def collect_roadmap_feedback(
        self,
        user_id: str,
        roadmap_id: str,
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Collect feedback after roadmap generation
        
        Args:
            user_id: User identifier
            roadmap_id: Roadmap identifier
            feedback: {
                "relevance_rating": int (1-5),
                "course_realistic": bool,
                "what_missing": str (optional),
                "what_unnecessary": str (optional),
                "additional_comments": str (optional)
            }
        
        Returns:
            Saved feedback record
        """
        database = get_database()
        feedback_collection = database["roadmap_feedback"]
        
        feedback_record = {
            "user_id": user_id,
            "roadmap_id": roadmap_id,
            "relevance_rating": feedback.get("relevance_rating", 0),
            "course_realistic": feedback.get("course_realistic", False),
            "what_missing": feedback.get("what_missing", ""),
            "what_unnecessary": feedback.get("what_unnecessary", ""),
            "additional_comments": feedback.get("additional_comments", ""),
            "timestamp": datetime.utcnow(),
            "feedback_type": "roadmap"
        }
        
        result = await feedback_collection.insert_one(feedback_record)
        feedback_record["_id"] = result.inserted_id
        
        return feedback_record
    
    async def get_feedback_summary(self, roadmap_id: str) -> Dict[str, Any]:
        """Get aggregated feedback summary for a roadmap"""
        database = get_database()
        feedback_collection = database["roadmap_feedback"]
        
        # Get all feedback for this roadmap
        feedbacks = await feedback_collection.find({"roadmap_id": roadmap_id}).to_list(length=100)
        
        if not feedbacks:
            return {
                "total_responses": 0,
                "average_relevance": 0,
                "realistic_percentage": 0
            }
        
        # Calculate statistics
        total = len(feedbacks)
        relevance_sum = sum(f.get("relevance_rating", 0) for f in feedbacks)
        realistic_count = sum(1 for f in feedbacks if f.get("course_realistic", False))
        
        return {
            "total_responses": total,
            "average_relevance": round(relevance_sum / total, 2) if total > 0 else 0,
            "realistic_percentage": round(realistic_count / total * 100, 2) if total > 0 else 0,
            "common_missing": self._extract_common_themes(feedbacks, "what_missing"),
            "common_unnecessary": self._extract_common_themes(feedbacks, "what_unnecessary")
        }
    
    def _extract_common_themes(self, feedbacks: List[Dict[str, Any]], field: str) -> List[str]:
        """Extract common themes from feedback text fields"""
        themes = []
        for feedback in feedbacks:
            text = feedback.get(field, "").strip()
            if text:
                themes.append(text)
        # Return top 3 most common (simplified - could use NLP for better extraction)
        return themes[:3]
    
    def generate_feedback_prompt(self) -> str:
        """Generate feedback collection prompt for frontend"""
        return """User Feedback (Optional):
1. Was this roadmap relevant? (1–5)
2. Were the course recommendations realistic? (Yes/No)
3. What felt missing?
4. What felt unnecessary?"""

# Global instance
feedback_system = FeedbackSystem()
