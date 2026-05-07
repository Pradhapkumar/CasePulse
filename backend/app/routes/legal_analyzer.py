from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.legal_analyzer_service import analyze_legal_query

router = APIRouter(prefix="/api/legal-sections", tags=["legal_analyzer"])

class AnalysisRequest(BaseModel):
    query: str

@router.post("/analyze")
def analyze_section(request: AnalysisRequest):
    result = analyze_legal_query(request.query)
    if not result["found"]:
        # We don't throw 404, we return the negative result for the UI to handle
        return result
    return result
