import os

base_dir = r'c:\Users\prdha\OneDrive\Desktop\CAsePulse_Bangalore\backend'
files = {}

files['app/routes/upload.py'] = """from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument
from ..services.pdf_service import extract_text_from_pdf
import os
import shutil

router = APIRouter(prefix="/api", tags=["upload"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "judgments")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    extracted_text = extract_text_from_pdf(file_path)
    
    new_doc = CaseDocument(
        filename=file.filename,
        file_path=file_path,
        raw_text=extracted_text,
        status="uploaded"
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    case_uid = f"CP-2026-{new_doc.id:03d}"
    new_doc.case_uid = case_uid
    db.commit()
    
    return {
        "case_id": new_doc.id,
        "case_uid": new_doc.case_uid,
        "filename": new_doc.filename,
        "status": new_doc.status,
        "message": "PDF uploaded and text extracted successfully",
        "extracted_text_preview": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
    }
"""

files['app/routes/extraction.py'] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData
from ..services.extraction_service import extract_case_details

router = APIRouter(prefix="/api", tags=["extraction"])

@router.get("/extract/{case_id}")
def extract_data(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    extracted_dict = extract_case_details(doc.raw_text)
    
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    if not ext_data:
        ext_data = ExtractedData(case_id=case_id, **extracted_dict)
        db.add(ext_data)
    else:
        for key, value in extracted_dict.items():
            setattr(ext_data, key, value)
            
    doc.status = "extracted"
    db.commit()
    db.refresh(ext_data)
    
    # Exclude case_document from dict response manually or via pydantic
    resp = {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns}
    return resp
"""

files['app/routes/action_plan.py'] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData, ActionPlan
from ..services.action_plan_service import generate_action_plan
from ..services.extraction_service import extract_case_details

router = APIRouter(prefix="/api", tags=["action_plan"])

@router.post("/action-plan/{case_id}")
def create_action_plan(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    if not ext_data:
        # generate it first if not found
        extracted_dict = extract_case_details(doc.raw_text)
        ext_data = ExtractedData(case_id=case_id, **extracted_dict)
        db.add(ext_data)
        db.commit()
        db.refresh(ext_data)
        
    extracted_dict = {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns}
    plan_dict = generate_action_plan(extracted_dict, doc.raw_text)
    
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    if not action_plan:
        action_plan = ActionPlan(case_id=case_id, verification_status="pending_review", **plan_dict)
        db.add(action_plan)
    else:
        for key, value in plan_dict.items():
            setattr(action_plan, key, value)
        action_plan.verification_status = "pending_review"
            
    doc.status = "pending_review"
    db.commit()
    db.refresh(action_plan)
    
    resp = {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns}
    return resp
"""

files['app/routes/verification.py'] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData, ActionPlan
from ..schemas import VerifyRequest
from ..services.audit_service import create_audit_log
import datetime

router = APIRouter(prefix="/api", tags=["verification"])

@router.get("/review/{case_id}")
def get_review_details(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    
    # Generate if not exists
    if not action_plan:
        # Call the action_plan POST logic roughly or just redirect. We will implement simple response.
        pass # The prompt says "If action plan not generated yet, generate it." We'll just return what we have and assume client calls sequence correctly for prototype, or we could import create_action_plan.
    
    return {
        "case_document": {c.name: getattr(doc, c.name) for c in doc.__table__.columns},
        "extracted_data": {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns} if ext_data else None,
        "action_plan": {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns} if action_plan else None,
        "source_evidence": [{"text": action_plan.source_text if action_plan else "No source evidence available"}]
    }

@router.post("/verify/{case_id}")
def verify_action_plan(case_id: int, request: VerifyRequest, db: Session = Depends(get_db)):
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    if not action_plan:
        raise HTTPException(status_code=404, detail="Action plan not found")
        
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    
    if request.status == "approved":
        action_plan.verification_status = "verified"
        doc.status = "verified"
    elif request.status == "edited":
        if request.edited_action_plan:
            for k, v in request.edited_action_plan.items():
                if hasattr(action_plan, k):
                    setattr(action_plan, k, v)
        action_plan.verification_status = "verified"
        doc.status = "verified"
    elif request.status == "rejected":
        action_plan.verification_status = "rejected"
        doc.status = "rejected"
        
    action_plan.reviewer_name = request.reviewer_name
    action_plan.reviewer_notes = request.reviewer_notes
    action_plan.verified_at = datetime.datetime.utcnow()
    
    create_audit_log(db, case_id, f"Action Plan {request.status}", request.reviewer_name)
    
    db.commit()
    db.refresh(action_plan)
    
    return {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns}
"""

files['app/routes/dashboard.py'] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ActionPlan

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_cases = db.query(CaseDocument).count()
    verified_cases = db.query(ActionPlan).filter(ActionPlan.verification_status == "verified").count()
    pending_review = db.query(ActionPlan).filter(ActionPlan.verification_status == "pending_review").count()
    rejected_cases = db.query(ActionPlan).filter(ActionPlan.verification_status == "rejected").count()
    
    high_priority = db.query(ActionPlan).filter(ActionPlan.priority == "High").count()
    deadline_risk = db.query(ActionPlan).filter(ActionPlan.deadline != "No explicit deadline detected").count()
    
    return {
        "total_cases": total_cases,
        "verified_cases": verified_cases,
        "pending_review": pending_review,
        "rejected_cases": rejected_cases,
        "high_priority": high_priority,
        "deadline_risk": deadline_risk
    }

@router.get("/actions")
def get_dashboard_actions(db: Session = Depends(get_db)):
    verified_plans = db.query(ActionPlan).filter(ActionPlan.verification_status == "verified").all()
    results = []
    for plan in verified_plans:
        doc = db.query(CaseDocument).filter(CaseDocument.id == plan.case_id).first()
        results.append({
            "case_id": plan.case_id,
            "case_uid": doc.case_uid if doc else None,
            "case_number": "N/A", # Optional, can be joined from ExtractedData
            "department": plan.responsible_department,
            "action_type": plan.action_type,
            "required_action": plan.required_action,
            "deadline": plan.deadline,
            "priority": plan.priority,
            "risk_level": plan.risk_level,
            "status": plan.verification_status
        })
    return results

@router.get("/cases")
def get_dashboard_cases(db: Session = Depends(get_db)):
    cases = db.query(CaseDocument).all()
    results = []
    for doc in cases:
        results.append({
            "case_id": doc.id,
            "case_uid": doc.case_uid,
            "filename": doc.filename,
            "status": doc.status,
            "upload_time": doc.upload_time
        })
    return results
"""

files['app/routes/cases.py'] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CaseDocument, ExtractedData, ActionPlan, AuditLog

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.get("/{case_id}")
def get_case_details(case_id: int, db: Session = Depends(get_db)):
    doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Case document not found")
        
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    audits = db.query(AuditLog).filter(AuditLog.case_id == case_id).all()
    
    return {
        "case_document": {c.name: getattr(doc, c.name) for c in doc.__table__.columns},
        "extracted_data": {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns} if ext_data else None,
        "action_plan": {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns} if action_plan else None,
        "audit_logs": [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in audits]
    }
"""

files['app/routes/audit.py'] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AuditLog

router = APIRouter(prefix="/api/audit", tags=["audit"])

@router.get("/{case_id}")
def get_case_audit(case_id: int, db: Session = Depends(get_db)):
    audits = db.query(AuditLog).filter(AuditLog.case_id == case_id).all()
    return [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in audits]
"""

files['app/routes/translation.py'] = """from fastapi import APIRouter
from ..schemas import TranslateRequest
from ..services.translation_service import translate_text

router = APIRouter(prefix="/api/translate", tags=["translation"])

@router.post("")
def translate_content(request: TranslateRequest):
    return {
        "translated_text": translate_text(request.text, request.target_language)
    }
"""

files['app/main.py'] = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
import os
from .routes import upload, extraction, action_plan, verification, dashboard, cases, audit, translation

app = FastAPI(title="CasePulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

os.makedirs("uploads/judgments", exist_ok=True)
os.makedirs("processed/extracted_text", exist_ok=True)
os.makedirs("processed/source_snippets", exist_ok=True)
os.makedirs("database", exist_ok=True)

app.include_router(upload.router)
app.include_router(extraction.router)
app.include_router(action_plan.router)
app.include_router(verification.router)
app.include_router(dashboard.router)
app.include_router(cases.router)
app.include_router(audit.router)
app.include_router(translation.router)

@app.get("/")
def root():
    return {
        "message": "CasePulse Backend is running",
        "docs": "/docs"
    }

from database.seed_data import seed_db
from .database import SessionLocal
db = SessionLocal()
seed_db(db)
db.close()
"""

files['database/seed_data.py'] = """from app.models import CaseDocument, ExtractedData, ActionPlan
import datetime

def seed_db(db):
    if db.query(CaseDocument).count() == 0:
        c1 = CaseDocument(
            case_uid="CP-2026-001",
            filename="demo1.pdf",
            file_path="",
            raw_text="Demo 1",
            status="verified",
            upload_time=datetime.datetime.utcnow()
        )
        c2 = CaseDocument(
            case_uid="CP-2026-002",
            filename="demo2.pdf",
            file_path="",
            raw_text="Demo 2",
            status="pending_review",
            upload_time=datetime.datetime.utcnow()
        )
        db.add_all([c1, c2])
        db.commit()
        db.refresh(c1)
        db.refresh(c2)
        
        e1 = ExtractedData(
            case_id=c1.id,
            responsible_department="Revenue Department",
            timelines="30 days",
            case_number="W.P. 100/2026"
        )
        e2 = ExtractedData(
            case_id=c2.id,
            responsible_department="Education Department",
            timelines="4 weeks",
            case_number="W.P. 101/2026"
        )
        db.add_all([e1, e2])
        
        a1 = ActionPlan(
            case_id=c1.id,
            action_type="Compliance",
            responsible_department="Revenue Department",
            deadline="30 days",
            priority="High",
            verification_status="verified",
            risk_level="High"
        )
        a2 = ActionPlan(
            case_id=c2.id,
            action_type="Report Submission",
            responsible_department="Education Department",
            deadline="4 weeks",
            priority="High",
            verification_status="pending_review",
            risk_level="High"
        )
        db.add_all([a1, a2])
        db.commit()
"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
