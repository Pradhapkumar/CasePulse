from sqlalchemy.orm import Session
from ..models import AuditLog
import datetime

def store_feedback_signal(db: Session, case_id: int, reviewer_status: str, reviewer_notes: str, edited_action_plan: dict):
    # This acts as a mock for human-in-the-loop learning
    # We store the correction in the audit log.
    action_desc = f"AI Feedback Signal: {reviewer_status}"
    
    notes = reviewer_notes or "No notes provided"
    
    log = AuditLog(
        case_id=case_id,
        action=action_desc,
        performed_by="System (Feedback Loop)",
        old_value="AI Generated Plan",
        new_value=f"Edited Plan: {edited_action_plan} | Notes: {notes}" if edited_action_plan else f"Notes: {notes}",
        timestamp=datetime.datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return "Reviewer feedback stored for future model improvement."

def generate_feedback_summary(case_id: int, old_action_plan: dict, edited_action_plan: dict) -> dict:
    changed_fields = []
    if not edited_action_plan:
        return {"changed_fields": [], "learning_signal": "No edits made"}
        
    for key, value in edited_action_plan.items():
        if key in old_action_plan and old_action_plan[key] != value:
            changed_fields.append(key)
            
    if changed_fields:
        signal = f"AI {', '.join(changed_fields)} extraction corrected by reviewer"
    else:
        signal = "AI output verified without edits"
        
    return {
        "changed_fields": changed_fields,
        "learning_signal": signal
    }
