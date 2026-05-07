from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData, ActionPlan
from ..schemas import VerifyRequest
from ..services.audit_service import create_audit_log
from ..services.feedback_learning_service import store_feedback_signal
import datetime
import json

router = APIRouter(prefix="/api", tags=["verification"])

@router.get("/review/{case_id}")
def get_review_details(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    
    # Generate ai_insights
    ai_insights = {}
    if action_plan:
        risk_factors = []
        if action_plan.risk_factors:
            try:
                risk_factors = json.loads(action_plan.risk_factors)
            except:
                risk_factors = []
                
        ai_insights = {
            "confidence_breakdown": {
                "overall_confidence": action_plan.confidence_score or 0
            },
            "risk_score": action_plan.risk_score or 0,
            "risk_factors": risk_factors,
            "detected_directions": [],
            "ml_pipeline": [
                "PDF Text Extraction",
                "Legal Entity Extraction",
                "Direction Classification",
                "Action Plan Classification",
                "Confidence Scoring",
                "Risk Scoring",
                "Human Verification"
            ]
        }
        
    return {
        "case_document": {c.name: getattr(doc, c.name) for c in doc.__table__.columns},
        "extracted_data": {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns} if ext_data else None,
        "action_plan": {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns} if action_plan else None,
        "source_evidence": [{"text": action_plan.source_text if action_plan else "No source evidence available"}],
        "ai_insights": ai_insights
    }

@router.post("/verify/{case_id}")
def verify_action_plan(case_id: int, request: VerifyRequest, db: Session = Depends(get_db)):
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    if not action_plan:
        raise HTTPException(status_code=404, detail="Action plan not found")
        
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    
    if request.status == "approved":
        action_plan.verification_status = "verified"
        doc.status = "verified"
    elif request.status == "edited":
        if request.edited_action_plan:
            for k, v in request.edited_action_plan.items():
                if hasattr(action_plan, k):
                    setattr(action_plan, k, v)
        action_plan.verification_status = "verified"
        doc.status = "verified"
    elif request.status == "rejected":
        action_plan.verification_status = "rejected"
        doc.status = "rejected"
        
    action_plan.reviewer_name = request.reviewer_name
    action_plan.reviewer_notes = request.reviewer_notes
    action_plan.verified_at = datetime.datetime.utcnow()
    
    create_audit_log(db, case_id, f"Action Plan {request.status}", request.reviewer_name)
    
    # Store feedback signal
    feedback_msg = store_feedback_signal(db, case_id, request.status, request.reviewer_notes or "", request.edited_action_plan or {})
    
    db.commit()
    db.refresh(action_plan)
    
    return {
        "message": "Verification completed",
        "feedback_signal": feedback_msg,
        "action_plan": {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns}
    }
