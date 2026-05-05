"""
Entity Extractor Module
Extracts named entities from case documents using NLP techniques
"""

from typing import List, Dict, Any
import re


class EntityExtractor:
    """Extract named entities from case documents"""

    def __init__(self):
        """Initialize entity extractor"""
        self.entity_types = [
            "PERSON",
            "ORGANIZATION",
            "LOCATION",
            "DATE",
            "MONEY",
            "LEGAL_CONCEPT"
        ]

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all entities from text
        
        Args:
            text: Input case document text
            
        Returns:
            List of extracted entities with type and position
        """
        entities = []
        
        # Extract different entity types
        entities.extend(self._extract_persons(text))
        entities.extend(self._extract_organizations(text))
        entities.extend(self._extract_locations(text))
        entities.extend(self._extract_dates(text))
        entities.extend(self._extract_money(text))
        entities.extend(self._extract_legal_concepts(text))
        
        return self._deduplicate_entities(entities)

    def _extract_persons(self, text: str) -> List[Dict[str, Any]]:
        """Extract person names"""
        persons = []
        # Pattern for capitalized names
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        for match in re.finditer(pattern, text):
            persons.append({
                "text": match.group(),
                "type": "PERSON",
                "start": match.start(),
                "end": match.end()
            })
        return persons

    def _extract_organizations(self, text: str) -> List[Dict[str, Any]]:
        """Extract organization names"""
        organizations = []
        keywords = ["Inc", "Ltd", "Corp", "Corporation", "Company", "LLC", "Bank"]
        
        for keyword in keywords:
            pattern = rf'\b\w+\s+{keyword}\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                organizations.append({
                    "text": match.group(),
                    "type": "ORGANIZATION",
                    "start": match.start(),
                    "end": match.end()
                })
        return organizations

    def _extract_locations(self, text: str) -> List[Dict[str, Any]]:
        """Extract location names"""
        locations = []
        # Common location patterns
        patterns = [
            r'\b(?:New York|California|Texas|Florida|Chicago|Los Angeles|Houston)\b',
            r'\b[A-Z][a-z]+,\s*[A-Z]{2}\b',  # City, State
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                locations.append({
                    "text": match.group(),
                    "type": "LOCATION",
                    "start": match.start(),
                    "end": match.end()
                })
        return locations

    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract dates"""
        dates = []
        patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # MM/DD/YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{4}-\d{1,2}-\d{1,2}\b'  # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                dates.append({
                    "text": match.group(),
                    "type": "DATE",
                    "start": match.start(),
                    "end": match.end()
                })
        return dates

    def _extract_money(self, text: str) -> List[Dict[str, Any]]:
        """Extract monetary amounts"""
        money = []
        # Match currency amounts
        pattern = r'[\$£€][\d,]+(?:\.\d{2})?|\b\d+\s*(?:dollars|euros|pounds)\b'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            money.append({
                "text": match.group(),
                "type": "MONEY",
                "start": match.start(),
                "end": match.end()
            })
        return money

    def _extract_legal_concepts(self, text: str) -> List[Dict[str, Any]]:
        """Extract legal concepts and terms"""
        concepts = []
        legal_terms = [
            "negligence", "breach", "contract", "liability", "damages",
            "plaintiff", "defendant", "defendant", "verdict", "settlement",
            "injunction", "lawsuit", "litigation", "appeal"
        ]
        
        for term in legal_terms:
            pattern = rf'\b{term}\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                concepts.append({
                    "text": match.group(),
                    "type": "LEGAL_CONCEPT",
                    "start": match.start(),
                    "end": match.end()
                })
        return concepts

    def _deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entities"""
        seen = set()
        unique = []
        
        for entity in entities:
            key = (entity['text'], entity['type'])
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return sorted(unique, key=lambda x: x['start'])
