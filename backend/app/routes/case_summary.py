from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.case_summary_service import generate_case_summary
from ..models import CaseSummary, CaseDocument, ExtractedData, ActionPlan
from typing import Dict, Any

router = APIRouter()

@router.post("/generate/{case_id}")
def generate_summary(case_id: int, db: Session = Depends(get_db)):
    result = generate_case_summary(db, case_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{case_uid}")
def get_summary(case_uid: str, db: Session = Depends(get_db)):
    summary = db.query(CaseSummary).filter(CaseSummary.case_uid == case_uid).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Case summary not found")
    
    # Also fetch linked data
    case_doc = db.query(CaseDocument).filter(CaseDocument.id == summary.case_id).first()
    
    return {
        "case_summary": summary,
        "extracted_data": case_doc.extracted_data if case_doc else None,
        "action_plan": case_doc.action_plan if case_doc else None,
        "audit_logs": case_doc.audit_logs if case_doc else []
    }

@router.get("/qr/{case_uid}")
def get_qr_info(case_uid: str, db: Session = Depends(get_db)):
    summary = db.query(CaseSummary).filter(CaseSummary.case_uid == case_uid).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Case summary not found")
    return {
        "case_uid": case_uid,
        "qr_url": summary.qr_url
    }
