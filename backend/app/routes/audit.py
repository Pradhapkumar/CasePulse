from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AuditLog

router = APIRouter(prefix="/api/audit", tags=["audit"])

@router.get("/{case_id}")
def get_case_audit(case_id: int, db: Session = Depends(get_db)):
    audits = db.query(AuditLog).filter(AuditLog.case_id == case_id).all()
    return [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in audits]
