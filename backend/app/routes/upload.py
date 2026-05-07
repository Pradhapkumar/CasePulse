from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
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
