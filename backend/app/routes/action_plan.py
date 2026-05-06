"""
Action Plan Route — /api/action-plan
--------------------------------------
POST /api/action-plan/generate     → Generate action plan from extracted data
GET  /api/action-plan/{case_id}    → Retrieve stored action plan for a case
"""

import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.services.action_plan_service import ActionGenerator

router = APIRouter()
_generator = ActionGenerator()


class ActionPlanRequest(BaseModel):
    case_id:        str
    extracted_data: dict


@router.post("/generate")
async def generate_action_plan(
    request: ActionPlanRequest,
    db:      Session = Depends(get_db),
):
    """
    Generate an action plan based on previously extracted case data
    and persist it back to the Case record.
    """
    case = db.query(Case).filter(Case.id == request.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    try:
        action_plan = _generator.generate(request.extracted_data)

        # Persist to DB
        case.action_plan = json.dumps(action_plan)
        case.updated_at  = datetime.utcnow()
        db.commit()
        db.refresh(case)

        return JSONResponse({
            "success":     True,
            "case_id":     request.case_id,
            "action_plan": action_plan,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_action_plan(case_id: str, db: Session = Depends(get_db)):
    """Retrieve the action plan stored for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    return JSONResponse({
        "case_id":     case.id,
        "action_plan": json.loads(case.action_plan) if case.action_plan else {},
        "status":      case.status,
    })
