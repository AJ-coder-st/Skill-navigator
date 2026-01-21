"""
Citation Formatter - Source Citation & Traceability
Formats citations for all course recommendations and learning resources
"""

from typing import Dict, Any, List, Optional

class CitationFormatter:
    """Formats citations for courses and learning resources"""
    
    @staticmethod
    def format_course_citation(course: Dict[str, Any]) -> str:
        """
        Format a course citation in standard format
        
        Format: Platform – Course Name (URL)
        Example: Coursera – SQL for Data Science (https://www.coursera.org/learn/sql-for-data-science)
        """
        course_name = course.get("resource_name", "Unknown Course")
        provider = course.get("provider", "Unknown Platform")
        url = course.get("url", "")
        
        if url:
            return f"{provider} – {course_name} ({url})"
        else:
            return f"{provider} – {course_name}"
    
    @staticmethod
    def format_course_citation_full(course: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format full citation object for a course
        
        Returns:
            {
                "course_name": str,
                "platform": str,
                "provider": str,
                "url": str,
                "citation": str,
                "source": str
            }
        """
        course_name = course.get("resource_name", "Unknown Course")
        provider = course.get("provider", "Unknown Platform")
        url = course.get("url", "")
        
        citation = CitationFormatter.format_course_citation(course)
        
        return {
            "course_name": course_name,
            "platform": provider,
            "provider": provider,
            "url": url,
            "citation": citation,
            "source": citation  # Alias for compatibility
        }
    
    @staticmethod
    def format_milestone_resources(courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format resources for roadmap milestones with citations
        
        Returns list of resource objects with citations
        """
        resources = []
        
        for course in courses:
            resource = CitationFormatter.format_course_citation_full(course)
            resources.append(resource)
        
        return resources
    
    @staticmethod
    def format_roadmap_citations(roadmap: Dict[str, Any], course_mapping: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Add citations to roadmap milestones
        
        Args:
            roadmap: The roadmap dictionary
            course_mapping: Mapping of skills to courses
            
        Returns:
            Roadmap with citations added to milestones
        """
        if "weeks" not in roadmap:
            return roadmap
        
        for week in roadmap.get("weeks", []):
            if "milestones" not in week:
                continue
            
            for milestone in week["milestones"]:
                skills_covered = milestone.get("skills_covered", [])
                cited_resources = []
                
                # Find courses for each skill
                for skill in skills_covered:
                    if skill in course_mapping:
                        for course in course_mapping[skill]:
                            cited_resources.append(
                                CitationFormatter.format_course_citation_full(course)
                            )
                
                # Add citations to milestone
                if cited_resources:
                    milestone["resources_cited"] = cited_resources
                    milestone["resources"] = [
                        f"{r['course_name']} ({r['platform']})" 
                        for r in cited_resources
                    ]
        
        return roadmap

# Global instance
citation_formatter = CitationFormatter()
