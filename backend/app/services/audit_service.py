from ..models import AuditLog
from sqlalchemy.orm import Session
import datetime

def create_audit_log(db: Session, case_id: int, action: str, performed_by: str, old_value: str = None, new_value: str = None):
    audit = AuditLog(
        case_id=case_id,
        action=action,
        performed_by=performed_by,
        old_value=old_value,
        new_value=new_value,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
