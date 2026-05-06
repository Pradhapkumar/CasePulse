"""
Action Generator Service
Generates action plans based on extracted case data
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta


class ActionGenerator:
    """Service for generating action plans from case data"""

    def __init__(self):
        """Initialize action generator"""
        self.priority_levels = ["High", "Medium", "Low"]

    def generate(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate action plan based on extracted case data
        
        Args:
            extracted_data: Dictionary containing extracted case information
            
        Returns:
            Dictionary with generated action plan
        """
        action_plan = {
            "plan_id": self._generate_plan_id(),
            "actions": self._generate_actions(extracted_data),
            "timeline": self._generate_timeline(extracted_data),
            "priorities": self._prioritize_actions(extracted_data),
            "generated_at": datetime.now().isoformat(),
            "status": "active"
        }
        return action_plan

    def _generate_plan_id(self) -> str:
        """Generate unique plan identifier"""
        return f"PLAN_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _generate_actions(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific actions based on case data"""
        actions = []

        # Add analysis action
        actions.append({
            "id": "action_1",
            "title": "Conduct Detailed Case Analysis",
            "description": "Review all case documents and identify key issues",
            "status": "pending",
            "assigned_to": None,
            "due_date": (datetime.now() + timedelta(days=3)).isoformat()
        })

        # Add research action
        actions.append({
            "id": "action_2",
            "title": "Legal Research",
            "description": "Research relevant case law and precedents",
            "status": "pending",
            "assigned_to": None,
            "due_date": (datetime.now() + timedelta(days=5)).isoformat()
        })

        # Add documentation action
        actions.append({
            "id": "action_3",
            "title": "Document Preparation",
            "description": "Prepare necessary legal documents",
            "status": "pending",
            "assigned_to": None,
            "due_date": (datetime.now() + timedelta(days=7)).isoformat()
        })

        return actions

    def _generate_timeline(self, extracted_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate timeline for action plan"""
        today = datetime.now()
        return {
            "start_date": today.isoformat(),
            "initial_phase": (today + timedelta(days=7)).isoformat(),
            "research_phase": (today + timedelta(days=14)).isoformat(),
            "preparation_phase": (today + timedelta(days=21)).isoformat(),
            "estimated_completion": (today + timedelta(days=30)).isoformat()
        }

    def _prioritize_actions(self, extracted_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Prioritize actions based on case urgency"""
        priorities = []

        # Check for urgent legal issues
        legal_issues = extracted_data.get("legal_issues", [])
        urgent_issues = ["fraud", "emergency", "appeal_deadline"]

        for issue in legal_issues:
            if any(urgent in issue.lower() for urgent in urgent_issues):
                priorities.append({
                    "issue": issue,
                    "priority": "High",
                    "action": "Urgent legal review required"
                })

        return priorities
