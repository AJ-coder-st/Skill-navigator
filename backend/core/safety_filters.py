"""
Safety Filters & Output Moderation
Applies safety checks before final output: hallucination detection, bias checks, career realism
"""

from typing import Dict, Any, List, Optional
import re

class SafetyFilters:
    """Applies safety filters to AI outputs"""
    
    # Forbidden phrases that indicate hallucination or unrealistic claims
    FORBIDDEN_PHRASES = [
        "guaranteed job",
        "guaranteed salary",
        "100% success",
        "guaranteed placement",
        "guaranteed interview",
        "guaranteed offer",
        "instant job",
        "get hired immediately"
    ]
    
    # Low confidence indicators
    UNCERTAINTY_INDICATORS = [
        "might",
        "possibly",
        "perhaps",
        "could potentially",
        "may vary"
    ]
    
    def __init__(self):
        self.warnings = []
    
    def check_hallucination(self, text: str) -> Dict[str, Any]:
        """
        Check for potential hallucination indicators
        
        Returns:
            {
                "has_hallucination": bool,
                "confidence": str,  # "high", "medium", "low"
                "issues": List[str]
            }
        """
        issues = []
        text_lower = text.lower()
        
        # Check for forbidden phrases
        for phrase in self.FORBIDDEN_PHRASES:
            if phrase in text_lower:
                issues.append(f"Contains unrealistic claim: '{phrase}'")
        
        # Check for uncertainty indicators (might indicate low confidence)
        uncertainty_count = sum(1 for indicator in self.UNCERTAINTY_INDICATORS if indicator in text_lower)
        
        if issues:
            return {
                "has_hallucination": True,
                "confidence": "low",
                "issues": issues
            }
        elif uncertainty_count > 3:
            return {
                "has_hallucination": False,
                "confidence": "medium",
                "issues": ["High uncertainty in recommendations"]
            }
        else:
            return {
                "has_hallucination": False,
                "confidence": "high",
                "issues": []
            }
    
    def check_career_realism(self, text: str) -> Dict[str, Any]:
        """
        Check for unrealistic career claims
        
        Returns:
            {
                "is_realistic": bool,
                "warnings": List[str]
            }
        """
        warnings = []
        text_lower = text.lower()
        
        # Check for guaranteed outcomes
        if any(phrase in text_lower for phrase in ["guaranteed", "100%", "always", "never fails"]):
            warnings.append("Contains unrealistic guarantees")
        
        # Check for specific salary claims
        salary_pattern = r'\$\d+[kK]|\$\d+,\d+'
        if re.search(salary_pattern, text):
            warnings.append("Contains specific salary claims - should be validated")
        
        return {
            "is_realistic": len(warnings) == 0,
            "warnings": warnings
        }
    
    def check_bias(self, text: str) -> Dict[str, Any]:
        """
        Check for potential bias or harmful advice
        
        Returns:
            {
                "has_bias": bool,
                "issues": List[str]
            }
        """
        issues = []
        text_lower = text.lower()
        
        # Check for discriminatory language (basic check)
        bias_indicators = [
            "only for",
            "not suitable for",
            "requires specific",
            "exclusive to"
        ]
        
        for indicator in bias_indicators:
            if indicator in text_lower:
                # Context-dependent, so just flag for review
                issues.append(f"Potential bias indicator: '{indicator}'")
        
        return {
            "has_bias": len(issues) > 0,
            "issues": issues
        }
    
    def apply_safety_wrapper(self, content: Dict[str, Any], text_fields: List[str] = None) -> Dict[str, Any]:
        """
        Apply all safety checks and add warnings to content
        
        Args:
            content: The content dictionary to check
            text_fields: List of field names to check (default: ["reasoning", "overall_assessment"])
        
        Returns:
            Content with safety warnings added
        """
        if text_fields is None:
            text_fields = ["reasoning", "overall_assessment", "description"]
        
        all_warnings = []
        confidence_levels = []
        
        # Check all text fields
        for field in text_fields:
            if field in content:
                text = str(content[field])
                
                # Hallucination check
                hallucination_check = self.check_hallucination(text)
                confidence_levels.append(hallucination_check["confidence"])
                
                if hallucination_check["has_hallucination"]:
                    all_warnings.extend(hallucination_check["issues"])
                
                # Career realism check
                realism_check = self.check_career_realism(text)
                all_warnings.extend(realism_check["warnings"])
                
                # Bias check
                bias_check = self.check_bias(text)
                if bias_check["has_bias"]:
                    all_warnings.extend(bias_check["issues"])
        
        # Determine overall confidence
        if "low" in confidence_levels:
            overall_confidence = "low"
        elif "medium" in confidence_levels:
            overall_confidence = "medium"
        else:
            overall_confidence = "high"
        
        # Add safety warnings to content
        if all_warnings or overall_confidence != "high":
            content["safety_warnings"] = all_warnings
            content["confidence_level"] = overall_confidence
            
            # Add disclaimer based on confidence
            if overall_confidence == "low":
                content["safety_disclaimer"] = (
                    "⚠️ Note: This recommendation is based on limited data and should be validated "
                    "with a domain expert."
                )
            elif overall_confidence == "medium":
                content["safety_disclaimer"] = (
                    "⚠️ Some skills may vary depending on industry and region. "
                    "Please validate recommendations with industry professionals."
                )
        
        return content
    
    def generate_safety_disclaimer(self, confidence: str = "medium") -> str:
        """Generate appropriate safety disclaimer based on confidence level"""
        if confidence == "low":
            return (
                "⚠️ Note: This recommendation is based on limited data and should be validated "
                "with a domain expert."
            )
        elif confidence == "medium":
            return (
                "⚠️ Some skills may vary depending on industry and region. "
                "Please validate recommendations with industry professionals."
            )
        else:
            return (
                "ℹ️ Recommendations are based on current industry standards. "
                "Individual results may vary."
            )

# Global instance
safety_filters = SafetyFilters()
