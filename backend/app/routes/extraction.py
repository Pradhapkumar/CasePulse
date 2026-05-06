"""
Extraction Route — /api/extract
--------------------------------
POST /api/extract/{case_id}  → Run full AI pipeline on an uploaded PDF
GET  /api/extract/{case_id}  → Retrieve previously extracted data from DB
"""

import json
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Case
from app.services.pdf_service        import PDFReader
from app.services.ocr_service        import OCRService
from app.services.extraction_service import NLPExtractor
from app.services.department_mapper  import DepartmentMapper
from app.services.deadline_service   import DeadlineService
from app.services.confidence_service import ConfidenceService
from app.services.risk_service       import RiskService
from app.services.highlight_service  import HighlightService

router = APIRouter()

_pdf        = PDFReader()
_ocr        = OCRService()
_nlp        = NLPExtractor()
_dept       = DepartmentMapper()
_deadline   = DeadlineService()
_confidence = ConfidenceService()
_risk       = RiskService()
_highlight  = HighlightService()


@router.post("/{case_id}")
async def extract_data(case_id: str, db: Session = Depends(get_db)):
    """
    Run the full AI/NLP extraction pipeline on an uploaded case PDF.

    Pipeline:
        1. Load PDF from disk
        2. Text extraction (PyPDF2 or OCR fallback)
        3. NLP extraction  → case_number, parties, directions, dates
        4. Department detection
        5. Deadline detection
        6. Risk assessment
        7. Confidence score
        8. Source highlights
        9. Persist all results to DB
    """
    # ── 1. Load Case record ────────────────────────────────────────────
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    file_path = case.file_path
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found on disk.")

    try:
        # ── 2. Extract text ───────────────────────────────────────────
        if case.is_scanned:
            raw_text = _ocr.extract_with_fallback(file_path)
        else:
            raw_text = _pdf.extract_text(file_path)

        # ── 3. NLP Extraction ─────────────────────────────────────────
        extracted = _nlp.extract(raw_text)

        # ── 4. Department Detection ───────────────────────────────────
        department = _dept.detect(raw_text)
        extracted["department"] = department

        # ── 5. Deadline Detection ─────────────────────────────────────
        deadlines = _deadline.extract(raw_text)
        extracted["deadlines"] = deadlines

        # ── 6. Risk Assessment ────────────────────────────────────────
        risk_report = _risk.assess(deadlines)
        extracted["risk_level"] = risk_report["overall_risk"]

        # ── 7. Confidence Score ───────────────────────────────────────
        conf_report = _confidence.get_report(extracted)
        extracted["confidence_score"] = conf_report["score"]
        extracted["confidence_label"] = conf_report["label"]

        # ── 8. Source Highlights ──────────────────────────────────────
        highlights = _highlight.get_highlights(case_id)

        # ── 9. Persist to DB ──────────────────────────────────────────
        case.raw_text         = raw_text
        case.case_number      = extracted.get("case_number")
        case.petitioner       = str(extracted.get("parties", {}).get("plaintiffs", []))
        case.respondent       = str(extracted.get("parties", {}).get("defendants", []))
        case.directions       = str(extracted.get("legal_issues", []))
        case.department       = department
        case.deadlines        = json.dumps(deadlines)
        case.risk_level       = risk_report["overall_risk"]
        case.confidence_score = conf_report["score"]
        case.confidence_label = conf_report["label"]
        case.highlights       = json.dumps(highlights)
        case.status           = "extracted"
        case.updated_at       = datetime.utcnow()

        db.commit()
        db.refresh(case)

        return JSONResponse({
            "success":          True,
            "case_id":          case_id,
            "extracted_data":   extracted,
            "risk_report":      risk_report,
            "confidence_report": conf_report,
            "deadlines":        deadlines,
            "department":       department,
            "highlights":       highlights,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.get("/{case_id}")
async def get_extracted_data(case_id: str, db: Session = Depends(get_db)):
    """Retrieve previously extracted and stored data for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    return JSONResponse({
        "case_id":          case.id,
        "case_number":      case.case_number,
        "petitioner":       case.petitioner,
        "respondent":       case.respondent,
        "department":       case.department,
        "directions":       case.directions,
        "deadlines":        json.loads(case.deadlines)   if case.deadlines   else [],
        "highlights":       json.loads(case.highlights)  if case.highlights  else [],
        "risk_level":       case.risk_level,
        "confidence_score": case.confidence_score,
        "confidence_label": case.confidence_label,
        "status":           case.status,
    })
