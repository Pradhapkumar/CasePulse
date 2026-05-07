from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData, ActionPlan, AuditLog

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.get("/{case_id}")
def get_case_details(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    audits = db.query(AuditLog).filter(AuditLog.case_id == case_id).all()
    
    return {
        "case_document": {c.name: getattr(doc, c.name) for c in doc.__table__.columns},
        "extracted_data": {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns} if ext_data else None,
        "action_plan": {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns} if action_plan else None,
        "audit_logs": [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in audits]
    }
