"""
Pydantic schemas for data validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CaseBase(BaseModel):
    """Base model for case data"""
    title: str
    description: Optional[str] = None
    case_number: Optional[str] = None


class CaseCreate(CaseBase):
    """Schema for creating a new case"""
    pass


class Case(CaseBase):
    """Schema for case response"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExtractedDataSchema(BaseModel):
    """Schema for extracted case data"""
    case_number: Optional[str] = None
    dates: List[str] = []
    parties: Dict[str, List[str]] = {}
    legal_issues: List[str] = []
    key_facts: List[str] = []
    judgement: Optional[str] = None
    confidence_score: float = 0.0


class ActionPlanSchema(BaseModel):
    """Schema for action plan"""
    plan_id: str
    actions: List[Dict[str, Any]] = []
    timeline: Dict[str, str] = {}
    priorities: List[Dict[str, str]] = []
    generated_at: str
    status: str


class HighlightSchema(BaseModel):
    """Schema for document highlight"""
    id: str
    case_id: str
    text: str
    page: int
    color: str = "yellow"
    annotation: Optional[str] = None
    created_by: Optional[str] = None
    created_at: str
    type: str = "general"


class VerificationSchema(BaseModel):
    """Schema for verification record"""
    case_id: str
    data: Dict[str, Any]
    verified_by: str
    status: str = "verified"
    timestamp: Optional[str] = None


class DashboardStatsSchema(BaseModel):
    """Schema for dashboard statistics"""
    total_cases: int = 0
    processed: int = 0
    pending: int = 0
    verified: int = 0
    failed: int = 0
    avg_processing_time: float = 0.0


class UploadResponseSchema(BaseModel):
    """Schema for upload response"""
    success: bool
    case_id: str
    filename: str
    file_path: str
    pages: int
    message: str
