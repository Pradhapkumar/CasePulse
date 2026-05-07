from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseSummary, CaseDocument
from typing import List

router = APIRouter()

@router.get("/case/{case_uid}")
def search_case(case_uid: str, db: Session = Depends(get_db)):
    summary = db.query(CaseSummary).filter(CaseSummary.case_uid == case_uid).first()
    if not summary:
        # Try finding by CaseDocument case_uid as fallback
        doc = db.query(CaseDocument).filter(CaseDocument.case_uid == case_uid).first()
        if doc and doc.action_plan:
            # Maybe summary isn't generated yet?
            raise HTTPException(status_code=404, detail="Case found but summary not yet generated. Please review it first.")
        raise HTTPException(status_code=404, detail="Case not found in CasePulse database")
    
    case_doc = db.query(CaseDocument).filter(CaseDocument.id == summary.case_id).first()
    
    return {
        "case_summary": summary,
        "extracted_data": case_doc.extracted_data if case_doc else None,
        "action_plan": case_doc.action_plan if case_doc else None,
        "audit_logs": case_doc.audit_logs if case_doc else [],
        "status": case_doc.status if case_doc else "Unknown"
    }
