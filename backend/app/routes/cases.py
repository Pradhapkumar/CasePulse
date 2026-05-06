"""
Cases Route — /api/cases
--------------------------
GET  /api/cases/               → List all cases (with filters)
GET  /api/cases/{case_id}      → Full detail for one case
DELETE /api/cases/{case_id}    → Delete a case and its file
"""

import json
import os

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Case
from app.services.audit_service import AuditService, AuditAction

router = APIRouter()
_audit = AuditService()


@router.get("/")
async def list_cases(
    status:     Optional[str] = Query(default=None, description="Filter by status: pending/extracted/approved/rejected"),
    department: Optional[str] = Query(default=None, description="Filter by department name"),
    risk_level: Optional[str] = Query(default=None, description="Filter by risk: High/Medium/Low"),
    limit:      int           = Query(default=50, ge=1, le=200),
    offset:     int           = Query(default=0, ge=0),
    db:         Session       = Depends(get_db),
):
    """
    List all cases with optional filters.
    Returns summary data for dashboard use.
    """
    query = db.query(Case)

    if status:
        query = query.filter(Case.status == status)
    if department:
        query = query.filter(Case.department.ilike(f"%{department}%"))
    if risk_level:
        query = query.filter(Case.risk_level == risk_level)

    total = query.count()
    cases = query.order_by(Case.created_at.desc()).offset(offset).limit(limit).all()

    return JSONResponse({
        "total":  total,
        "offset": offset,
        "limit":  limit,
        "cases": [_case_summary(c) for c in cases],
    })


@router.get("/{case_id}")
async def get_case_detail(case_id: str, db: Session = Depends(get_db)):
    """Return full details for a single case including all extracted data."""
    case = _get_case_or_404(db, case_id)

    return JSONResponse({
        "id":               case.id,
        "case_number":      case.case_number,
        "court_name":       case.court_name,
        "petitioner":       case.petitioner,
        "respondent":       case.respondent,
        "department":       case.department,
        "directions":       case.directions,
        "action_plan":      json.loads(case.action_plan)  if case.action_plan  else {},
        "deadlines":        json.loads(case.deadlines)    if case.deadlines    else [],
        "highlights":       json.loads(case.highlights)   if case.highlights   else [],
        "risk_level":       case.risk_level,
        "confidence_score": case.confidence_score,
        "confidence_label": case.confidence_label,
        "status":           case.status,
        "reviewed_by":      case.reviewed_by,
        "review_notes":     case.review_notes,
        "file_name":        case.file_name,
        "is_scanned":       case.is_scanned,
        "created_at":       case.created_at.isoformat() if case.created_at else None,
        "updated_at":       case.updated_at.isoformat() if case.updated_at else None,
    })


@router.delete("/{case_id}")
async def delete_case(
    case_id:     str,
    officer_id:  str = Query(..., description="ID of officer performing deletion"),
    officer_name:str = Query(..., description="Name of officer performing deletion"),
    db:          Session = Depends(get_db),
):
    """Delete a case record and remove the associated PDF from disk."""
    case = _get_case_or_404(db, case_id)

    # Log the deletion before removing record
    _audit.log(
        db,
        case_id      = case_id,
        officer_id   = officer_id,
        officer_name = officer_name,
        action       = AuditAction.DELETE,
        notes        = f"Case {case.case_number or case_id} deleted.",
    )

    # Delete file from disk
    if case.file_path and os.path.exists(case.file_path):
        try:
            os.remove(case.file_path)
        except OSError:
            pass  # File already gone — proceed with DB cleanup

    db.delete(case)
    db.commit()

    return JSONResponse({
        "success":  True,
        "case_id":  case_id,
        "message":  "Case and associated file deleted successfully.",
    })


# ── Helpers ────────────────────────────────────────────────────────────────

def _get_case_or_404(db: Session, case_id: str) -> Case:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")
    return case


def _case_summary(case: Case) -> dict:
    """Lightweight summary dict for list views."""
    return {
        "id":               case.id,
        "case_number":      case.case_number,
        "petitioner":       case.petitioner,
        "respondent":       case.respondent,
        "department":       case.department,
        "risk_level":       case.risk_level,
        "confidence_score": case.confidence_score,
        "status":           case.status,
        "file_name":        case.file_name,
        "created_at":       case.created_at.isoformat() if case.created_at else None,
    }
