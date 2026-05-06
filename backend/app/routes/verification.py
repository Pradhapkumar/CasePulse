"""
Verification Route — /api/verify
----------------------------------
POST /api/verify/approve/{case_id}  → Officer approves a case
POST /api/verify/reject/{case_id}   → Officer rejects a case
POST /api/verify/edit/{case_id}     → Officer edits extracted fields
GET  /api/verify/{case_id}          → Get review status of a case
"""

from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.services.audit_service import AuditService, AuditAction

router = APIRouter()
_audit = AuditService()


# ── Request schemas ───────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    officer_id:   str
    officer_name: str
    notes:        Optional[str] = None


class EditRequest(BaseModel):
    officer_id:     str
    officer_name:   str
    changed_fields: Dict[str, Any]
    notes:          Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/approve/{case_id}")
async def approve_case(
    case_id: str,
    body:    ReviewRequest,
    db:      Session = Depends(get_db),
):
    """Officer approves the AI-extracted case data."""
    case = _get_case_or_404(db, case_id)

    case.status      = "approved"
    case.reviewed_by = body.officer_id
    case.review_notes = body.notes
    case.updated_at  = datetime.utcnow()
    db.commit()

    _audit.log(
        db,
        case_id      = case_id,
        officer_id   = body.officer_id,
        officer_name = body.officer_name,
        action       = AuditAction.APPROVE,
        notes        = body.notes,
    )

    return JSONResponse({
        "success":      True,
        "case_id":      case_id,
        "status":       "approved",
        "reviewed_by":  body.officer_name,
        "timestamp":    datetime.utcnow().isoformat(),
    })


@router.post("/reject/{case_id}")
async def reject_case(
    case_id: str,
    body:    ReviewRequest,
    db:      Session = Depends(get_db),
):
    """Officer rejects the case (e.g., wrong document uploaded)."""
    case = _get_case_or_404(db, case_id)

    case.status       = "rejected"
    case.reviewed_by  = body.officer_id
    case.review_notes = body.notes
    case.updated_at   = datetime.utcnow()
    db.commit()

    _audit.log(
        db,
        case_id      = case_id,
        officer_id   = body.officer_id,
        officer_name = body.officer_name,
        action       = AuditAction.REJECT,
        notes        = body.notes,
    )

    return JSONResponse({
        "success":     True,
        "case_id":     case_id,
        "status":      "rejected",
        "reviewed_by": body.officer_name,
        "timestamp":   datetime.utcnow().isoformat(),
    })


@router.post("/edit/{case_id}")
async def edit_case(
    case_id: str,
    body:    EditRequest,
    db:      Session = Depends(get_db),
):
    """
    Officer manually edits extracted fields.
    Allowed fields: case_number, petitioner, respondent,
                    department, directions, review_notes
    """
    case = _get_case_or_404(db, case_id)

    ALLOWED = {
        "case_number", "petitioner", "respondent",
        "department", "directions", "review_notes",
    }
    updated = {}
    for field, value in body.changed_fields.items():
        if field in ALLOWED:
            setattr(case, field, value)
            updated[field] = value

    case.status     = "edited"
    case.reviewed_by = body.officer_id
    case.updated_at = datetime.utcnow()
    db.commit()

    _audit.log(
        db,
        case_id        = case_id,
        officer_id     = body.officer_id,
        officer_name   = body.officer_name,
        action         = AuditAction.EDIT,
        notes          = body.notes,
        changed_fields = updated,
    )

    return JSONResponse({
        "success":        True,
        "case_id":        case_id,
        "status":         "edited",
        "updated_fields": updated,
        "reviewed_by":    body.officer_name,
        "timestamp":      datetime.utcnow().isoformat(),
    })


@router.get("/{case_id}")
async def get_verification_status(case_id: str, db: Session = Depends(get_db)):
    """Return current review status and reviewer info for a case."""
    case = _get_case_or_404(db, case_id)
    return JSONResponse({
        "case_id":      case.id,
        "status":       case.status,
        "reviewed_by":  case.reviewed_by,
        "review_notes": case.review_notes,
        "updated_at":   case.updated_at.isoformat() if case.updated_at else None,
    })


# ── Helper ────────────────────────────────────────────────────────────────────

def _get_case_or_404(db: Session, case_id: str) -> Case:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")
    return case
