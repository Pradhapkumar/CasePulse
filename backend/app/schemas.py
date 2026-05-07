from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class VerifyRequest(BaseModel):
    status: str
    reviewer_name: str
    reviewer_notes: Optional[str] = None
    edited_action_plan: Optional[Dict[str, Any]] = None

class TranslateRequest(BaseModel):
    text: str
    target_language: str

class ExtractedDataResponse(BaseModel):
    id: int
    case_id: int
    case_number: Optional[str]
    court_name: Optional[str]
    date_of_order: Optional[str]
    petitioner: Optional[str]
    respondent: Optional[str]
    parties_involved: Optional[str]
    key_directions: Optional[str]
    timelines: Optional[str]
    responsible_department: Optional[str]
    important_keywords: Optional[str]
    confidence_score: Optional[int]
    source_snippets: Optional[str]
    case_type: Optional[str]
    judgment_date: Optional[str]
    hearings_count: Optional[str]
    legal_sections: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True

class CaseSummaryResponse(BaseModel):
    id: int
    case_id: int
    case_uid: str
    case_title: Optional[str]
    case_type: Optional[str]
    case_number: Optional[str]
    court_name: Optional[str]
    judgment_date: Optional[str]
    petitioner: Optional[str]
    respondent: Optional[str]
    hearings_count: Optional[str]
    related_department: Optional[str]
    action_type: Optional[str]
    required_action: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]
    risk_level: Optional[str]
    confidence_score: Optional[int]
    source_evidence: Optional[str]
    summary_text: Optional[str]
    qr_url: Optional[str]
    legal_sections: Optional[List[Dict[str, Any]]]
    created_at: datetime

    class Config:
        from_attributes = True

class ActionPlanResponse(BaseModel):
    id: int
    case_id: int
    action_type: Optional[str]
    required_action: Optional[str]
    responsible_department: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]
    risk_level: Optional[str]
    reason: Optional[str]
    source_text: Optional[str]
    confidence_score: Optional[int]
    risk_score: Optional[int]
    risk_factors: Optional[str]
    verification_status: Optional[str]
    reviewer_name: Optional[str]
    reviewer_notes: Optional[str]
    verified_at: Optional[datetime]

    class Config:
        from_attributes = True

class DashboardSummaryResponse(BaseModel):
    total_cases: int
    verified_cases: int
    pending_review: int
    rejected_cases: int
    high_priority: int
    deadline_risk: int

class DashboardActionResponse(BaseModel):
    case_id: int
    case_uid: str
    case_number: Optional[str]
    department: Optional[str]
    action_type: Optional[str]
    required_action: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]
    risk_level: Optional[str]
    status: str

class DashboardCaseResponse(BaseModel):
    case_id: int
    case_uid: str
    filename: Optional[str]
    status: str
    upload_time: datetime

class ReviewResponse(BaseModel):
    case_document: Dict[str, Any]
    extracted_data: Optional[Dict[str, Any]]
    action_plan: Optional[Dict[str, Any]]
    source_evidence: List[Dict[str, Any]]
    ai_insights: Optional[Dict[str, Any]] = None

# Auth Schemas
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

