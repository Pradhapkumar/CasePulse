import datetime
from sqlalchemy.orm import Session
from ..models import CaseDocument, ExtractedData, ActionPlan, CaseSummary
from .extraction_service import extract_case_details

def generate_case_uid(db: Session) -> str:
    year = datetime.datetime.now().year
    count = db.query(CaseSummary).count()
    uid = f"CP-{year}-{str(count + 1).zfill(4)}"
    return uid

def build_summary_text(data: dict) -> str:
    case_type = data.get("case_type", "General")
    court = data.get("court_name", "the Court")
    petitioner = data.get("petitioner", "Petitioner")
    respondent = data.get("respondent", "Respondent")
    judgment_date = data.get("judgment_date", "N/A")
    dept = data.get("related_department", "the concerned department")
    action = data.get("action_type", "Action")
    deadline = data.get("deadline", "within the specified period")
    priority = data.get("priority", "Medium")

    summary = (
        f"This is a {case_type} case before {court}. "
        f"The petitioner {petitioner} filed against {respondent}. "
        f"The judgment dated {judgment_date} directs {dept} to perform {action} {deadline}. "
        f"The case requires compliance with {priority} priority."
    )
    return summary

def generate_case_summary(db: Session, case_id: int) -> dict:
    case_doc = db.query(CaseDocument).filter(CaseDocument.id == case_id).first()
    if not case_doc:
        return {"error": "Case not found"}

    # Ensure extracted data exists
    extracted_data = case_doc.extracted_data
    if not extracted_data:
        # Fallback to extraction if missing
        extraction_result = extract_case_details(case_doc.raw_text)
        new_extracted = ExtractedData(case_id=case_id, **extraction_result)
        db.add(new_extracted)
        db.commit()
        db.refresh(case_doc)
        extracted_data = case_doc.extracted_data

    # Load action plan
    action_plan = case_doc.action_plan
    if not action_plan:
        return {"error": "Action plan not found. Please review and approve first."}

    # Generate or reuse UID
    case_uid = case_doc.case_uid or generate_case_uid(db)
    if not case_doc.case_uid:
        case_doc.case_uid = case_uid
        db.commit()

    # Create CaseSummary entry
    existing_summary = db.query(CaseSummary).filter(CaseSummary.case_id == case_id).first()
    
    summary_data = {
        "case_id": case_id,
        "case_uid": case_uid,
        "case_title": f"{extracted_data.petitioner} vs {extracted_data.respondent}" if extracted_data.petitioner and extracted_data.respondent else "Case Title Not Detected",
        "case_type": extracted_data.case_type or "General",
        "case_number": extracted_data.case_number or "N/A",
        "court_name": extracted_data.court_name or "N/A",
        "judgment_date": extracted_data.judgment_date or "N/A",
        "petitioner": extracted_data.petitioner or "N/A",
        "respondent": extracted_data.respondent or "N/A",
        "hearings_count": extracted_data.hearings_count or "Not clearly mentioned",
        "related_department": action_plan.responsible_department or "Manual Verification",
        "action_type": action_plan.action_type or "Action",
        "required_action": action_plan.required_action or "...",
        "deadline": action_plan.deadline or "N/A",
        "priority": action_plan.priority or "Medium",
        "risk_level": action_plan.risk_level or "Low",
        "confidence_score": action_plan.confidence_score or 0,
        "source_evidence": action_plan.source_text or "",
        "summary_text": "", # Built below
        "qr_url": f"http://localhost:3000/public/case/{case_uid}",
        "legal_sections": extracted_data.legal_sections
    }
    
    summary_data["summary_text"] = build_summary_text(summary_data)
    summary_data["message"] = "Case summary generated successfully"

    if existing_summary:
        for key, value in summary_data.items():
            if key != "message": # Don't try to save message to DB
                setattr(existing_summary, key, value)
    else:
        # Create a copy without the message for DB
        db_data = {k: v for k, v in summary_data.items() if k != "message"}
        existing_summary = CaseSummary(**db_data)
        db.add(existing_summary)
    
    db.commit()
    db.refresh(existing_summary)
    
    return summary_data
