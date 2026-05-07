import os

base_dir = r'c:\Users\prdha\OneDrive\Desktop\CAsePulse_Bangalore\backend'

files = {}

files['requirements.txt'] = """fastapi
uvicorn
sqlalchemy
pydantic
python-multipart
pymupdf
"""

files['README.md'] = """# CasePulse Backend

## Project:
CasePulse Backend

## Setup:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## API testing order:
1. GET /
2. POST /api/upload
3. GET /api/extract/{case_id}
4. POST /api/action-plan/{case_id}
5. GET /api/review/{case_id}
6. POST /api/verify/{case_id}
7. GET /api/dashboard/summary
8. GET /api/dashboard/actions
"""

files['sample_judgment_text.txt'] = """IN THE HIGH COURT OF KARNATAKA AT BENGALURU

W.P. No. 1234/2026

Petitioner: Ramesh Kumar
Respondent: Revenue Department

ORDER

The respondent Revenue Department is directed to consider the petitioner application and pass appropriate orders within 30 days from the date of receipt of this order.

The department shall submit a compliance report before the next hearing.
"""

files['app/database.py'] = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
os.makedirs(DB_DIR, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'casepulse.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

files['app/models.py'] = """from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class CaseDocument(Base):
    __tablename__ = "case_documents"

    id = Column(Integer, primary key=True, index=True)
    case_uid = Column(String, unique=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    raw_text = Column(Text)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    extracted_data = relationship("ExtractedData", back_populates="case_document", uselist=False)
    action_plan = relationship("ActionPlan", back_populates="case_document", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="case_document")

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    case_number = Column(String)
    court_name = Column(String)
    date_of_order = Column(String)
    petitioner = Column(String)
    respondent = Column(String)
    parties_involved = Column(Text)
    key_directions = Column(Text)
    timelines = Column(String)
    responsible_department = Column(String)
    important_keywords = Column(Text)
    confidence_score = Column(Integer)
    source_snippets = Column(Text)

    case_document = relationship("CaseDocument", back_populates="extracted_data")

class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(Integer, primary key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    action_type = Column(String)
    required_action = Column(Text)
    responsible_department = Column(String)
    deadline = Column(String)
    priority = Column(String)
    risk_level = Column(String)
    reason = Column(Text)
    source_text = Column(Text)
    confidence_score = Column(Integer)
    verification_status = Column(String)
    reviewer_name = Column(String, nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    verified_at = Column(DateTime, nullable=True)

    case_document = relationship("CaseDocument", back_populates="action_plan")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    action = Column(String)
    performed_by = Column(String)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    case_document = relationship("CaseDocument", back_populates="audit_logs")
"""

files['app/schemas.py'] = """from pydantic import BaseModel
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

"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
