from app.models import CaseDocument, ExtractedData, ActionPlan
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
