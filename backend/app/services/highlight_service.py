"""
Highlight Service
Manages highlighting and annotation of important case information
"""

from typing import List, Dict, Any
from datetime import datetime


class HighlightService:
    """Service for managing highlights and annotations in case documents"""

    def __init__(self):
        """Initialize highlight service"""
        self.highlights = {}

    def add_highlight(self, case_id: str, highlight_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a highlight to a case document
        
        Args:
            case_id: The case identifier
            highlight_data: Dictionary containing highlight information
            
        Returns:
            Created highlight object
        """
        highlight = {
            "id": self._generate_highlight_id(),
            "case_id": case_id,
            "text": highlight_data.get("text"),
            "page": highlight_data.get("page"),
            "color": highlight_data.get("color", "yellow"),
            "annotation": highlight_data.get("annotation"),
            "created_by": highlight_data.get("created_by"),
            "created_at": datetime.now().isoformat(),
            "type": highlight_data.get("type", "general")  # e.g., "important", "query", "general"
        }

        if case_id not in self.highlights:
            self.highlights[case_id] = []

        self.highlights[case_id].append(highlight)
        return highlight

    def get_highlights(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Get all highlights for a case
        
        Args:
            case_id: The case identifier
            
        Returns:
            List of highlights for the case
        """
        return self.highlights.get(case_id, [])

    def update_highlight(self, case_id: str, highlight_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing highlight
        
        Args:
            case_id: The case identifier
            highlight_id: The highlight identifier
            updates: Dictionary with updates
            
        Returns:
            Updated highlight object
        """
        if case_id in self.highlights:
            for highlight in self.highlights[case_id]:
                if highlight["id"] == highlight_id:
                    highlight.update(updates)
                    highlight["updated_at"] = datetime.now().isoformat()
                    return highlight
        return None

    def delete_highlight(self, case_id: str, highlight_id: str) -> bool:
        """
        Delete a highlight
        
        Args:
            case_id: The case identifier
            highlight_id: The highlight identifier
            
        Returns:
            True if deleted, False otherwise
        """
        if case_id in self.highlights:
            self.highlights[case_id] = [
                h for h in self.highlights[case_id]
                if h["id"] != highlight_id
            ]
            return True
        return False

    def _generate_highlight_id(self) -> str:
        """Generate unique highlight identifier"""
        import uuid
        return str(uuid.uuid4())
