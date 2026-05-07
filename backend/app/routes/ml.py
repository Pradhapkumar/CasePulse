from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ActionPlan

router = APIRouter(prefix="/api/ml", tags=["ml"])

@router.get("/pipeline/{case_id}")
def get_ml_pipeline_status(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    
    verification_status = "pending_review"
    if action_plan and action_plan.verification_status:
        if action_plan.verification_status == "verified":
            verification_status = "completed"
        elif action_plan.verification_status == "rejected":
            verification_status = "rejected"
            
    # Mocking pipeline steps for demonstration
    pipeline = [
        {
            "step": "PDF Text Extraction",
            "status": "completed" if doc.raw_text else "pending",
            "description": "Judgment PDF converted into raw text"
        },
        {
            "step": "Legal Entity Extraction",
            "status": "completed" if doc.extracted_data else "pending",
            "description": "Case number, parties, court and date extracted"
        },
        {
            "step": "Direction Classification",
            "status": "completed" if doc.extracted_data else "pending",
            "description": "Court directions classified into compliance/report/appeal categories"
        },
        {
            "step": "Action Plan Generation",
            "status": "completed" if action_plan else "pending",
            "description": "Structured government action plan generated"
        },
        {
            "step": "Confidence Scoring",
            "status": "completed" if doc.extracted_data else "pending",
            "description": "AI confidence score calculated from entity, action and evidence signals"
        },
        {
            "step": "Risk Scoring",
            "status": "completed" if action_plan else "pending",
            "description": "Compliance risk estimated based on deadline, priority and confidence"
        },
        {
            "step": "Human Verification",
            "status": verification_status,
            "description": "Legal officer must approve, edit or reject before dashboard use"
        }
    ]
    
    return {
        "case_id": case_id,
        "pipeline": pipeline
    }
