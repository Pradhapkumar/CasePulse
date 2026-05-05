from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.action_generator import ActionGenerator

router = APIRouter()
action_generator = ActionGenerator()


class ActionPlanRequest(BaseModel):
    case_id: str
    extracted_data: dict


@router.post("/generate")
async def generate_action_plan(request: ActionPlanRequest):
    """
    Generate action plan based on extracted case data
    """
    try:
        action_plan = action_generator.generate(request.extracted_data)

        return JSONResponse({
            "success": True,
            "case_id": request.case_id,
            "action_plan": action_plan
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_action_plan(case_id: str):
    """
    Retrieve action plan for a case
    """
    try:
        # TODO: Implement database retrieval
        return JSONResponse({
            "case_id": case_id,
            "action_plan": {}
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
