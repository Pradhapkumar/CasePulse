"""
NLP Extractor Service
Extracts structured information from case documents using NLP
"""

import re
from typing import Dict, List, Any


class NLPExtractor:
    """Service for extracting structured data using NLP techniques"""

    def __init__(self):
        """Initialize NLP extractor"""
        self.case_keywords = ["case", "lawsuit", "litigation", "claim"]
        self.party_keywords = ["plaintiff", "defendant", "appellant", "respondent"]
        self.date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b'

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract structured information from case text
        
        Args:
            text: Raw text from case document
            
        Returns:
            Dictionary with extracted structured data
        """
        extracted = {
            "case_number": self._extract_case_number(text),
            "dates": self._extract_dates(text),
            "parties": self._extract_parties(text),
            "legal_issues": self._extract_legal_issues(text),
            "key_facts": self._extract_key_facts(text),
            "judgement": self._extract_judgement(text),
            "confidence_score": 0.75
        }
        return extracted

    def _extract_case_number(self, text: str) -> str:
        """Extract case number/identifier"""
        # Look for common case number patterns
        pattern = r'(?:Case No\.|Case #|#|No\.)\s*([A-Za-z0-9\-/]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_dates(self, text: str) -> List[str]:
        """Extract important dates from text"""
        dates = re.findall(self.date_pattern, text)
        return list(set(dates))

    def _extract_parties(self, text: str) -> Dict[str, List[str]]:
        """Extract parties involved in the case"""
        return {
            "plaintiffs": [],
            "defendants": [],
            "other_parties": []
        }

    def _extract_legal_issues(self, text: str) -> List[str]:
        """Extract main legal issues"""
        # This is a simplified implementation
        issues = []
        keywords = ["negligence", "breach", "contract", "fraud", "liability", "damages"]
        for keyword in keywords:
            if keyword.lower() in text.lower():
                issues.append(keyword)
        return issues

    def _extract_key_facts(self, text: str) -> List[str]:
        """Extract key facts from the case"""
        # This would typically use more advanced NLP
        sentences = text.split('.')
        key_facts = [s.strip() for s in sentences if len(s.strip()) > 50]
        return key_facts[:5]  # Return top 5 key facts

    def _extract_judgement(self, text: str) -> str:
        """Extract judgement or ruling"""
        judgement_keywords = ["judgment", "ruled", "held", "decided", "verdict"]
        for keyword in judgement_keywords:
            if keyword.lower() in text.lower():
                idx = text.lower().find(keyword)
                return text[max(0, idx-50):min(len(text), idx+200)]
        return None
