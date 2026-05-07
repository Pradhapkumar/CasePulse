from fastapi import APIRouter, Depends, HTTPException
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
        ext_model_columns = {c.name for c in ExtractedData.__table__.columns}
        filtered_ext_dict = {k: v for k, v in extracted_dict.items() if k in ext_model_columns}
        ext_data = ExtractedData(case_id=case_id, **filtered_ext_dict)
        db.add(ext_data)
        db.commit()
        db.refresh(ext_data)
        
    extracted_dict = {c.name: getattr(ext_data, c.name) for c in ext_data.__table__.columns}
    plan_dict = generate_action_plan(extracted_dict, doc.raw_text)
    
    plan_model_columns = {c.name for c in ActionPlan.__table__.columns}
    filtered_plan_dict = {k: v for k, v in plan_dict.items() if k in plan_model_columns}
    
    action_plan = db.query(ActionPlan).filter(ActionPlan.case_id == case_id).first()
    if not action_plan:
        action_plan = ActionPlan(case_id=case_id, verification_status="pending_review", **filtered_plan_dict)
        db.add(action_plan)
    else:
        for key, value in filtered_plan_dict.items():
            setattr(action_plan, key, value)
        action_plan.verification_status = "pending_review"
            
    doc.status = "pending_review"
    db.commit()
    db.refresh(action_plan)
    
    resp = {c.name: getattr(action_plan, c.name) for c in action_plan.__table__.columns}
    return resp
