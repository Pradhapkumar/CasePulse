from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_reader import PDFReader
from app.utils.helpers import generate_id
import os

router = APIRouter()
pdf_reader = PDFReader()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for case processing
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        case_id = generate_id()
        file_path = os.path.join(UPLOAD_FOLDER, f"{case_id}.pdf")

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract basic info
        pdf_info = pdf_reader.get_pdf_info(file_path)

        return JSONResponse({
            "success": True,
            "case_id": case_id,
            "filename": file.filename,
            "file_path": file_path,
            "pages": pdf_info.get("pages", 0),
            "message": "PDF uploaded successfully"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}")
async def get_upload_status(case_id: str):
    """
    Get upload status for a case
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, f"{case_id}.pdf")
        if os.path.exists(file_path):
            return JSONResponse({
                "case_id": case_id,
                "status": "uploaded",
                "file_path": file_path
            })
        else:
            raise HTTPException(status_code=404, detail="Case not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
