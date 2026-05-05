"""
Action Builder Module
Constructs action items from case analysis and NLP insights
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum


class ActionPriority(Enum):
    """Priority levels for actions"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionBuilder:
    """Build and construct action items from case data"""

    def __init__(self):
        """Initialize action builder"""
        self.action_counter = 0

    def build_actions(self, case_data: Dict[str, Any], 
                     extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Build action items from case and extracted data
        
        Args:
            case_data: Original case information
            extracted_data: NLP extracted data including keywords and entities
            
        Returns:
            List of constructed action items
        """
        actions = []
        
        # Generate actions based on case type
        actions.extend(self._generate_analysis_actions(case_data, extracted_data))
        
        # Generate actions based on legal issues
        actions.extend(self._generate_legal_issue_actions(extracted_data))
        
        # Generate actions based on parties involved
        actions.extend(self._generate_party_actions(extracted_data))
        
        # Prioritize and assign IDs
        actions = self._prioritize_actions(actions)
        actions = self._assign_action_ids(actions)
        
        return actions

    def _generate_analysis_actions(self, case_data: Dict[str, Any], 
                                   extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate initial analysis actions"""
        actions = []
        
        actions.append({
            "title": "Conduct Preliminary Case Review",
            "description": "Review all case documents and identify key issues and parties",
            "category": "analysis",
            "priority": ActionPriority.HIGH.value,
            "due_days": 3,
            "estimated_hours": 4
        })
        
        actions.append({
            "title": "Document Case Summary",
            "description": "Create comprehensive summary of case facts and legal claims",
            "category": "documentation",
            "priority": ActionPriority.HIGH.value,
            "due_days": 5,
            "estimated_hours": 3
        })
        
        return actions

    def _generate_legal_issue_actions(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actions based on legal issues identified"""
        actions = []
        legal_issues = extracted_data.get("legal_issues", [])
        
        # Map legal issues to specific actions
        issue_action_map = {
            "negligence": {
                "title": "Research Duty of Care Standards",
                "description": "Research applicable duty of care standards and precedents",
                "priority": ActionPriority.HIGH.value,
                "due_days": 7,
                "estimated_hours": 6
            },
            "breach": {
                "title": "Analyze Breach Elements",
                "description": "Detailed analysis of alleged breach and contractual obligations",
                "priority": ActionPriority.HIGH.value,
                "due_days": 7,
                "estimated_hours": 5
            },
            "fraud": {
                "title": "Examine Fraudulent Conduct Claims",
                "description": "Investigate fraud allegations and supporting evidence",
                "priority": ActionPriority.CRITICAL.value,
                "due_days": 3,
                "estimated_hours": 8
            },
            "damages": {
                "title": "Calculate Damages Assessment",
                "description": "Prepare detailed damages calculation and valuation",
                "priority": ActionPriority.HIGH.value,
                "due_days": 10,
                "estimated_hours": 6
            }
        }
        
        for issue in legal_issues:
            if issue.lower() in issue_action_map:
                action_template = issue_action_map[issue.lower()]
                actions.append({
                    "title": action_template["title"],
                    "description": action_template["description"],
                    "category": "legal_research",
                    "priority": action_template["priority"],
                    "due_days": action_template["due_days"],
                    "estimated_hours": action_template["estimated_hours"]
                })
        
        return actions

    def _generate_party_actions(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actions based on parties involved"""
        actions = []
        parties = extracted_data.get("parties", {})
        
        if parties.get("defendants"):
            actions.append({
                "title": "Investigate Defendant Background",
                "description": "Research defendant's history and financial status",
                "category": "investigation",
                "priority": ActionPriority.MEDIUM.value,
                "due_days": 7,
                "estimated_hours": 4
            })
        
        if parties.get("plaintiffs"):
            actions.append({
                "title": "Verify Plaintiff Claims",
                "description": "Verify authenticity and validity of plaintiff's claims",
                "category": "verification",
                "priority": ActionPriority.HIGH.value,
                "due_days": 5,
                "estimated_hours": 3
            })
        
        return actions

    def _prioritize_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize actions based on urgency and dependencies"""
        priority_order = {
            ActionPriority.CRITICAL.value: 0,
            ActionPriority.HIGH.value: 1,
            ActionPriority.MEDIUM.value: 2,
            ActionPriority.LOW.value: 3
        }
        
        # Sort by priority
        actions.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 4))
        
        # Add due dates
        for i, action in enumerate(actions):
            due_days = action.pop("due_days", 7)
            due_date = datetime.now() + timedelta(days=due_days)
            action["due_date"] = due_date.isoformat()
        
        return actions

    def _assign_action_ids(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign unique IDs to actions"""
        for i, action in enumerate(actions, 1):
            action["id"] = f"ACT_{i:03d}"
            action["status"] = "pending"
            action["created_at"] = datetime.now().isoformat()
        
        return actions

    def create_milestone(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create project milestone from actions
        
        Args:
            actions: List of actions
            
        Returns:
            Milestone object
        """
        total_hours = sum(a.get("estimated_hours", 0) for a in actions)
        
        milestone = {
            "milestone_id": f"MS_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "total_actions": len(actions),
            "total_estimated_hours": total_hours,
            "start_date": datetime.now().isoformat(),
            "target_completion": (datetime.now() + timedelta(days=30)).isoformat(),
            "actions": actions,
            "progress": 0
        }
        
        return milestone
