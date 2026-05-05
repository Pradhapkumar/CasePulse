"""
Keyword Detector Module
Detects important keywords and phrases in case documents
"""

from typing import List, Dict, Any
import re
from collections import Counter


class KeywordDetector:
    """Detect important keywords and phrases from case text"""

    def __init__(self):
        """Initialize keyword detector"""
        self.legal_keywords = {
            "negligence": {"category": "tort", "weight": 0.9},
            "breach": {"category": "contract", "weight": 0.85},
            "liability": {"category": "general", "weight": 0.8},
            "damages": {"category": "remedies", "weight": 0.8},
            "plaintiff": {"category": "party", "weight": 0.7},
            "defendant": {"category": "party", "weight": 0.7},
            "contract": {"category": "contract", "weight": 0.85},
            "agreement": {"category": "contract", "weight": 0.75},
            "violation": {"category": "violation", "weight": 0.8},
            "fraud": {"category": "tort", "weight": 0.95},
            "injunction": {"category": "remedy", "weight": 0.85},
            "settlement": {"category": "resolution", "weight": 0.8},
            "verdict": {"category": "judgment", "weight": 0.9},
            "appeal": {"category": "procedure", "weight": 0.7},
            "evidence": {"category": "procedure", "weight": 0.7},
        }

    def detect_keywords(self, text: str, top_n: int = 20) -> List[Dict[str, Any]]:
        """
        Detect important keywords from text
        
        Args:
            text: Input case document text
            top_n: Number of top keywords to return
            
        Returns:
            List of detected keywords with scores
        """
        keywords = []
        
        # Detect legal keywords
        keywords.extend(self._detect_legal_keywords(text))
        
        # Detect phrases
        keywords.extend(self._detect_phrases(text))
        
        # Score and rank keywords
        keywords = self._score_keywords(keywords)
        
        # Remove duplicates and return top N
        unique_keywords = {}
        for kw in keywords:
            key = kw['text'].lower()
            if key not in unique_keywords or kw['score'] > unique_keywords[key]['score']:
                unique_keywords[key] = kw
        
        return sorted(unique_keywords.values(), 
                     key=lambda x: x['score'], 
                     reverse=True)[:top_n]

    def _detect_legal_keywords(self, text: str) -> List[Dict[str, Any]]:
        """Detect known legal keywords"""
        keywords = []
        text_lower = text.lower()
        
        for keyword, metadata in self.legal_keywords.items():
            pattern = rf'\b{keyword}\b'
            count = len(re.findall(pattern, text_lower, re.IGNORECASE))
            
            if count > 0:
                keywords.append({
                    "text": keyword,
                    "type": "legal",
                    "category": metadata['category'],
                    "weight": metadata['weight'],
                    "frequency": count
                })
        
        return keywords

    def _detect_phrases(self, text: str) -> List[Dict[str, Any]]:
        """Detect important phrases"""
        phrases = []
        
        # Common legal phrases
        legal_phrases = [
            "duty of care",
            "reasonable person",
            "breach of contract",
            "material breach",
            "force majeure",
            "statute of limitations",
            "burden of proof",
            "preponderance of evidence",
            "beyond reasonable doubt"
        ]
        
        for phrase in legal_phrases:
            pattern = rf'\b{phrase}\b'
            count = len(re.findall(pattern, text, re.IGNORECASE))
            
            if count > 0:
                phrases.append({
                    "text": phrase,
                    "type": "phrase",
                    "category": "legal_phrase",
                    "weight": 0.85,
                    "frequency": count
                })
        
        return phrases

    def _score_keywords(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score keywords based on frequency and weight"""
        for keyword in keywords:
            frequency_score = min(keyword['frequency'] / 10, 1.0)  # Normalize frequency
            keyword['score'] = keyword['weight'] * (0.6 + 0.4 * frequency_score)
        
        return keywords

    def extract_context(self, text: str, keyword: str, context_window: int = 50) -> List[str]:
        """
        Extract context snippets around a keyword
        
        Args:
            text: Input text
            keyword: Keyword to find context for
            context_window: Number of characters around keyword
            
        Returns:
            List of context snippets
        """
        contexts = []
        pattern = rf'.{{0,{context_window}}}{keyword}.{{0,{context_window}}}'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            contexts.append(match.group().strip())
        
        return contexts

    def get_keyword_density(self, text: str) -> Dict[str, float]:
        """
        Calculate keyword density in text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of keyword densities
        """
        words = text.lower().split()
        total_words = len(words)
        
        keyword_counts = Counter(words)
        densities = {}
        
        for keyword in self.legal_keywords.keys():
            count = keyword_counts.get(keyword, 0)
            if count > 0:
                densities[keyword] = (count / total_words) * 100
        
        return densities
