from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseSummary

router = APIRouter()

@router.get("/case/{case_uid}")
def get_public_case(case_uid: str, db: Session = Depends(get_db)):
    summary = db.query(CaseSummary).filter(CaseSummary.case_uid == case_uid).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Return public-safe fields only
    return {
        "case_uid": summary.case_uid,
        "case_title": summary.case_title,
        "case_type": summary.case_type,
        "case_number": summary.case_number,
        "court_name": summary.court_name,
        "judgment_date": summary.judgment_date,
        "related_department": summary.related_department,
        "action_type": summary.action_type,
        "required_action": summary.required_action,
        "deadline": summary.deadline,
        "priority": summary.priority,
        "risk_level": summary.risk_level,
        "summary_text": summary.summary_text,
        "verification_status": "Verified" # Since summary is generated after review
    }
