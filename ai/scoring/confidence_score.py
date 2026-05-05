"""
Confidence Scoring Module
Calculates confidence scores for extracted data and predictions
"""

from typing import Dict, List, Any, Tuple
import math


class ConfidenceScorer:
    """Calculate confidence scores for extracted information"""

    def __init__(self):
        """Initialize confidence scorer"""
        self.score_weights = {
            "entity_recognition": 0.25,
            "keyword_frequency": 0.20,
            "pattern_matching": 0.20,
            "source_reliability": 0.15,
            "consistency": 0.20
        }

    def score_extraction(self, extracted_data: Dict[str, Any], 
                        source_text: str) -> Tuple[float, Dict[str, float]]:
        """
        Calculate overall confidence score for extracted data
        
        Args:
            extracted_data: Dictionary of extracted information
            source_text: Original source text
            
        Returns:
            Tuple of (overall_score, component_scores)
        """
        component_scores = {}
        
        # Score each component
        component_scores["entity_recognition"] = self._score_entity_recognition(extracted_data)
        component_scores["keyword_frequency"] = self._score_keyword_frequency(extracted_data)
        component_scores["pattern_matching"] = self._score_pattern_matching(extracted_data, source_text)
        component_scores["source_reliability"] = self._score_source_reliability(source_text)
        component_scores["consistency"] = self._score_consistency(extracted_data)
        
        # Calculate weighted overall score
        overall_score = sum(
            component_scores[key] * self.score_weights[key]
            for key in component_scores
        )
        
        return round(overall_score, 3), {k: round(v, 3) for k, v in component_scores.items()}

    def _score_entity_recognition(self, extracted_data: Dict[str, Any]) -> float:
        """Score quality of entity recognition"""
        entities = extracted_data.get("parties", {})
        
        # Count recognized entities
        entity_count = sum(len(v) if isinstance(v, list) else (1 if v else 0) 
                          for v in entities.values())
        
        # Normalize to 0-1 scale (expecting 2-5 entities typically)
        score = min(entity_count / 5, 1.0)
        
        return score

    def _score_keyword_frequency(self, extracted_data: Dict[str, Any]) -> float:
        """Score based on keyword and legal issue frequency"""
        legal_issues = extracted_data.get("legal_issues", [])
        
        # More identified legal issues = higher confidence
        score = min(len(legal_issues) / 5, 1.0)
        
        # Boost if multiple consistent issues found
        if len(legal_issues) > 2:
            score = min(score * 1.2, 1.0)
        
        return score

    def _score_pattern_matching(self, extracted_data: Dict[str, Any], 
                               source_text: str) -> float:
        """Score based on pattern matching accuracy"""
        case_number = extracted_data.get("case_number")
        dates = extracted_data.get("dates", [])
        
        score = 0.0
        max_score = 0.0
        
        # Case number pattern match
        if case_number:
            max_score += 0.5
            score += 0.5  # Case number found
        
        # Date pattern match
        max_score += 0.5
        if dates:
            score += 0.5 * min(len(dates) / 3, 1.0)  # Multiple dates boost
        
        return score if max_score == 0 else min(score / max_score, 1.0)

    def _score_source_reliability(self, source_text: str) -> float:
        """Score based on source document reliability"""
        # Assess text quality indicators
        text_length = len(source_text)
        paragraph_count = source_text.count('\n\n')
        
        score = 0.0
        
        # Good length = reliable source
        if text_length > 1000:
            score += 0.4
        elif text_length > 500:
            score += 0.2
        
        # Multiple paragraphs = structured document
        if paragraph_count > 3:
            score += 0.3
        elif paragraph_count > 0:
            score += 0.1
        
        # Check for legal language indicators
        legal_indicators = ["whereas", "thereof", "hereinafter", "plaintiff", "defendant"]
        indicator_count = sum(1 for indicator in legal_indicators 
                             if indicator.lower() in source_text.lower())
        
        score += 0.3 * min(indicator_count / 3, 1.0)
        
        return min(score, 1.0)

    def _score_consistency(self, extracted_data: Dict[str, Any]) -> float:
        """Score internal consistency of extracted data"""
        score = 1.0
        
        # Check for internal contradictions
        case_number = extracted_data.get("case_number")
        parties = extracted_data.get("parties", {})
        
        # Deduct if missing expected fields
        if not case_number:
            score -= 0.2
        
        if not parties:
            score -= 0.2
        
        # Ensure parties are reasonable
        plaintiff_count = len(parties.get("plaintiffs", []))
        defendant_count = len(parties.get("defendants", []))
        
        if plaintiff_count > 10 or defendant_count > 10:
            score -= 0.3  # Unlikely to have too many parties
        
        return max(score, 0.0)

    def score_action_relevance(self, action: Dict[str, Any], 
                              extracted_data: Dict[str, Any]) -> float:
        """
        Score relevance of an action to case data
        
        Args:
            action: Action item to score
            extracted_data: Extracted case data
            
        Returns:
            Relevance score 0-1
        """
        score = 0.5  # Base score
        
        legal_issues = extracted_data.get("legal_issues", [])
        action_title = action.get("title", "").lower()
        
        # Check keyword matches
        for issue in legal_issues:
            if issue.lower() in action_title:
                score += 0.2
        
        # Check category alignment
        action_category = action.get("category", "").lower()
        if any(x in action_category for x in ["legal", "research", "analysis"]):
            score += 0.15
        
        return min(score, 1.0)

    def calculate_overall_confidence(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate overall confidence level and recommendations
        
        Args:
            scores: Dictionary of component scores
            
        Returns:
            Confidence assessment with recommendations
        """
        values = list(scores.values())
        average_score = sum(values) / len(values) if values else 0
        
        # Determine confidence level
        if average_score >= 0.8:
            level = "high"
            recommendation = "Proceed with confidence"
        elif average_score >= 0.6:
            level = "medium"
            recommendation = "Review and verify key findings"
        elif average_score >= 0.4:
            level = "low"
            recommendation = "Manual review required"
        else:
            level = "very_low"
            recommendation = "Insufficient data for reliable extraction"
        
        return {
            "overall_score": round(average_score, 3),
            "confidence_level": level,
            "component_scores": scores,
            "recommendation": recommendation,
            "strongest_component": max(scores.items(), key=lambda x: x[1]),
            "weakest_component": min(scores.items(), key=lambda x: x[1])
        }
