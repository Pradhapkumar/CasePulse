from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class VerificationRequest(BaseModel):
    case_id: str
    data: dict
    verified_by: str


@router.post("/data")
async def verify_data(request: VerificationRequest):
    """
    Verify extracted case data
    """
    try:
        # TODO: Store verification in database
        return JSONResponse({
            "success": True,
            "case_id": request.case_id,
            "status": "verified",
            "verified_by": request.verified_by,
            "timestamp": None  # TODO: Add timestamp
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_verification_status(case_id: str):
    """
    Get verification status for a case
    """
    try:
        # TODO: Retrieve from database
        return JSONResponse({
            "case_id": case_id,
            "status": "pending",
            "verified_by": None
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
