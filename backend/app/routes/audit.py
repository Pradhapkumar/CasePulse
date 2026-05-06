"""
Audit Route — /api/audit
--------------------------
GET /api/audit/case/{case_id}       → Full audit trail for one case
GET /api/audit/officer/{officer_id} → All actions by one officer
GET /api/audit/recent               → Latest 50 actions (admin view)
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.audit_service import AuditService

router   = APIRouter()
_audit   = AuditService()


@router.get("/case/{case_id}")
async def get_case_audit_trail(
    case_id: str,
    limit:   int     = Query(default=100, ge=1, le=500),
    db:      Session = Depends(get_db),
):
    """Return full chronological audit history for a specific case."""
    logs = _audit.get_by_case(db, case_id=case_id, limit=limit)
    if logs is None:
        raise HTTPException(status_code=404, detail="No audit records found for this case.")
    return JSONResponse({
        "case_id":  case_id,
        "count":    len(logs),
        "records":  logs,
    })


@router.get("/officer/{officer_id}")
async def get_officer_audit_history(
    officer_id: str,
    limit:      int     = Query(default=100, ge=1, le=500),
    db:         Session = Depends(get_db),
):
    """Return all actions performed by a specific officer."""
    logs = _audit.get_by_officer(db, officer_id=officer_id, limit=limit)
    return JSONResponse({
        "officer_id": officer_id,
        "count":      len(logs),
        "records":    logs,
    })


@router.get("/recent")
async def get_recent_audit_activity(
    limit: int     = Query(default=50, ge=1, le=200),
    db:    Session = Depends(get_db),
):
    """Return the most recent audit entries across all cases (admin use)."""
    logs = _audit.get_recent(db, limit=limit)
    return JSONResponse({
        "count":   len(logs),
        "records": logs,
    })
