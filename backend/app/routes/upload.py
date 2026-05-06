"""
Upload Route — /api/upload
--------------------------
POST /api/upload/          → Upload a PDF, save to disk, return case_id
GET  /api/upload/{case_id} → Check upload status
"""

import os
import uuid
from datetime import datetime

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.services.pdf_service import PDFReader
from app.services.ocr_service import OCRService

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

_pdf_reader = PDFReader()
_ocr        = OCRService()


@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...),
    db:   Session    = Depends(get_db),
):
    """
    Upload a PDF file for case processing.
    Saves the file, creates a Case record, returns case_id.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        case_id   = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_FOLDER, f"{case_id}.pdf")

        # Save file to disk
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Get basic PDF metadata
        pdf_info   = _pdf_reader.get_pdf_info(file_path)
        is_scanned = _ocr.is_scanned_pdf(file_path)

        # Persist Case record
        case = Case(
            id         = case_id,
            file_name  = file.filename,
            file_path  = file_path,
            is_scanned = is_scanned,
            status     = "pending",
            created_at = datetime.utcnow(),
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        return JSONResponse({
            "success":    True,
            "case_id":    case_id,
            "filename":   file.filename,
            "pages":      pdf_info.get("pages", 0),
            "is_scanned": is_scanned,
            "status":     "pending",
            "message":    "PDF uploaded successfully. Ready for extraction.",
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_upload_status(case_id: str, db: Session = Depends(get_db)):
    """Return the upload status and metadata for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")
    return JSONResponse({
        "case_id":    case.id,
        "file_name":  case.file_name,
        "status":     case.status,
        "is_scanned": case.is_scanned,
        "created_at": case.created_at.isoformat() if case.created_at else None,
    })
