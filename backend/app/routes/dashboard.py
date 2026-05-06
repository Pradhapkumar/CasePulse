"""
Dashboard Route — /api/dashboard
----------------------------------
GET /api/dashboard/stats   → Aggregate case counts & risk summary
GET /api/dashboard/cases   → Paginated case list for dashboard table
GET /api/dashboard/recent-activity → Latest audit actions
"""

import json
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Case, AuditLog
from app.services.audit_service import AuditService

router = APIRouter()
_audit = AuditService()


@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Return live aggregate statistics for the dashboard overview cards.
    """
    try:
        total    = db.query(func.count(Case.id)).scalar() or 0
        pending  = db.query(func.count(Case.id)).filter(Case.status == "pending").scalar()   or 0
        extracted= db.query(func.count(Case.id)).filter(Case.status == "extracted").scalar() or 0
        approved = db.query(func.count(Case.id)).filter(Case.status == "approved").scalar()  or 0
        rejected = db.query(func.count(Case.id)).filter(Case.status == "rejected").scalar()  or 0
        edited   = db.query(func.count(Case.id)).filter(Case.status == "edited").scalar()    or 0

        # Risk breakdown
        high_risk   = db.query(func.count(Case.id)).filter(Case.risk_level == "High").scalar()   or 0
        medium_risk = db.query(func.count(Case.id)).filter(Case.risk_level == "Medium").scalar() or 0
        low_risk    = db.query(func.count(Case.id)).filter(Case.risk_level == "Low").scalar()    or 0

        # Avg confidence
        avg_conf_row = db.query(func.avg(Case.confidence_score)).scalar()
        avg_conf     = round(float(avg_conf_row), 2) if avg_conf_row else 0.0

        return JSONResponse({
            "success": True,
            "stats": {
                "total_cases":        total,
                "pending":            pending,
                "extracted":          extracted,
                "approved":           approved,
                "rejected":           rejected,
                "edited":             edited,
                "reviewed":           approved + rejected + edited,
                "risk_breakdown": {
                    "high":   high_risk,
                    "medium": medium_risk,
                    "low":    low_risk,
                },
                "avg_confidence_score": avg_conf,
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cases")
async def get_dashboard_cases(
    status:     Optional[str] = Query(default=None),
    risk_level: Optional[str] = Query(default=None),
    skip:       int           = Query(default=0, ge=0),
    limit:      int           = Query(default=10, ge=1, le=100),
    db:         Session       = Depends(get_db),
):
    """
    Paginated list of cases for the dashboard table.
    Supports filtering by status and risk level.
    """
    try:
        query = db.query(Case)
        if status:
            query = query.filter(Case.status == status)
        if risk_level:
            query = query.filter(Case.risk_level == risk_level)

        total = query.count()
        cases = query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()

        return JSONResponse({
            "success": True,
            "total":   total,
            "skip":    skip,
            "limit":   limit,
            "cases": [
                {
                    "id":               c.id,
                    "case_number":      c.case_number,
                    "petitioner":       c.petitioner,
                    "respondent":       c.respondent,
                    "department":       c.department,
                    "risk_level":       c.risk_level,
                    "confidence_score": c.confidence_score,
                    "confidence_label": c.confidence_label,
                    "status":           c.status,
                    "file_name":        c.file_name,
                    "created_at":       c.created_at.isoformat() if c.created_at else None,
                }
                for c in cases
            ],
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int     = Query(default=20, ge=1, le=100),
    db:    Session = Depends(get_db),
):
    """Return the most recent officer actions for the activity feed."""
    try:
        logs = _audit.get_recent(db, limit=limit)
        return JSONResponse({
            "success": True,
            "count":   len(logs),
            "records": logs,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/case/{case_id}")
async def get_case_detail_for_dashboard(case_id: str, db: Session = Depends(get_db)):
    """Return full case detail for dashboard drill-down view."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    return JSONResponse({
        "case_id":          case.id,
        "case_number":      case.case_number,
        "petitioner":       case.petitioner,
        "respondent":       case.respondent,
        "department":       case.department,
        "directions":       case.directions,
        "deadlines":        json.loads(case.deadlines)   if case.deadlines   else [],
        "action_plan":      json.loads(case.action_plan) if case.action_plan else {},
        "risk_level":       case.risk_level,
        "confidence_score": case.confidence_score,
        "confidence_label": case.confidence_label,
        "status":           case.status,
        "reviewed_by":      case.reviewed_by,
        "created_at":       case.created_at.isoformat() if case.created_at else None,
    })
