from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.nlp_extractor import NLPExtractor
from app.services.pdf_reader import PDFReader
import os

router = APIRouter()
nlp_extractor = NLPExtractor()
pdf_reader = PDFReader()

UPLOAD_FOLDER = "uploads"


@router.post("/{case_id}")
async def extract_data(case_id: str):
    """
    Extract data from uploaded PDF using NLP
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, f"{case_id}.pdf")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Case PDF not found")

        # Extract text from PDF
        pdf_text = pdf_reader.extract_text(file_path)

        # Extract structured data using NLP
        extracted_data = nlp_extractor.extract(pdf_text)

        return JSONResponse({
            "success": True,
            "case_id": case_id,
            "extracted_data": extracted_data
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_extracted_data(case_id: str):
    """
    Retrieve previously extracted data for a case
    """
    try:
        # TODO: Implement database retrieval
        return JSONResponse({
            "case_id": case_id,
            "data": {}
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
