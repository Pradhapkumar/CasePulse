from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ActionPlan

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_cases = db.query(CaseDocument).count()
    verified_cases = db.query(ActionPlan).filter(ActionPlan.verification_status == "verified").count()
    pending_review = db.query(ActionPlan).filter(ActionPlan.verification_status == "pending_review").count()
    rejected_cases = db.query(ActionPlan).filter(ActionPlan.verification_status == "rejected").count()
    
    high_priority = db.query(ActionPlan).filter(ActionPlan.priority == "High").count()
    deadline_risk = db.query(ActionPlan).filter(ActionPlan.deadline != "No explicit deadline detected").count()
    
    return {
        "total_cases": total_cases,
        "verified_cases": verified_cases,
        "pending_review": pending_review,
        "rejected_cases": rejected_cases,
        "high_priority": high_priority,
        "deadline_risk": deadline_risk
    }

@router.get("/actions")
def get_dashboard_actions(db: Session = Depends(get_db)):
    verified_plans = db.query(ActionPlan).filter(ActionPlan.verification_status == "verified").all()
    results = []
    for plan in verified_plans:
        doc = db.query(CaseDocument).filter(CaseDocument.id == plan.case_id).first()
        results.append({
            "case_id": plan.case_id,
            "case_uid": doc.case_uid if doc else None,
            "case_number": "N/A", # Optional, can be joined from ExtractedData
            "department": plan.responsible_department,
            "action_type": plan.action_type,
            "required_action": plan.required_action,
            "deadline": plan.deadline,
            "priority": plan.priority,
            "risk_level": plan.risk_level,
            "status": plan.verification_status
        })
    return results

@router.get("/cases")
def get_dashboard_cases(db: Session = Depends(get_db)):
    cases = db.query(CaseDocument).all()
    results = []
    for doc in cases:
        results.append({
            "case_id": doc.id,
            "case_uid": doc.case_uid,
            "filename": doc.filename,
            "status": doc.status,
            "upload_time": doc.upload_time
        })
    return results
