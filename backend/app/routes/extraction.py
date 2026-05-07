from fastapi import APIRouter, Depends, HTTPException
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
    
    model_columns = {c.name for c in ExtractedData.__table__.columns}
    filtered_dict = {k: v for k, v in extracted_dict.items() if k in model_columns}
    
    ext_data = db.query(ExtractedData).filter(ExtractedData.case_id == case_id).first()
    if not ext_data:
        ext_data = ExtractedData(case_id=case_id, **filtered_dict)
        db.add(ext_data)
    else:
        for key, value in filtered_dict.items():
            setattr(ext_data, key, value)
            
    doc.status = "extracted"
    db.commit()
    db.refresh(ext_data)
    
    # Exclude case_document from dict response manually or via pydantic
    resp = {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns}
    return resp
