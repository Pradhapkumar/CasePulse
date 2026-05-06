"""
Seed Database
Populate the database with initial/dummy data for testing and UI development.
"""
import sys
import os
import uuid
import json
from datetime import datetime, timedelta

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Case, AuditLog
from app.services.audit_service import AuditAction

def seed():
    db = SessionLocal()
    print("Seeding database...")
    
    # Check if data already exists
    if db.query(Case).count() > 0:
        print("Database already contains data. Run reset_db.py first if you want to re-seed.")
        db.close()
        return

    # Create dummy cases
    case1_id = str(uuid.uuid4())
    case1 = Case(
        id=case1_id,
        case_number="WP-2023-4451",
        court_name="High Court of Karnataka",
        petitioner="['Ramesh Kumar']",
        respondent="['State of Karnataka']",
        department="Revenue Department",
        status="pending",
        risk_level="High",
        confidence_score=0.85,
        confidence_label="High",
        file_name="petition_ramesh.pdf",
        file_path="uploads/petition_ramesh.pdf",
        deadlines=json.dumps([
            {"raw_text": "within 7 days", "type": "relative", "days": 7, "due_date": (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d"), "snippet": "respondent to file objections within 7 days"}
        ]),
        created_at=datetime.utcnow() - timedelta(days=2)
    )

    case2_id = str(uuid.uuid4())
    case2 = Case(
        id=case2_id,
        case_number="OS-2024-112",
        court_name="District Court Bangalore",
        petitioner="['Priya Sharma']",
        respondent="['BBMP']",
        department="Municipal Administration",
        status="approved",
        risk_level="Medium",
        confidence_score=0.92,
        confidence_label="High",
        file_name="bbmp_notice.pdf",
        file_path="uploads/bbmp_notice.pdf",
        reviewed_by="OFF-001",
        created_at=datetime.utcnow() - timedelta(days=5),
        updated_at=datetime.utcnow() - timedelta(days=1)
    )

    db.add(case1)
    db.add(case2)
    db.commit()

    # Add audit logs
    log1 = AuditLog(
        case_id=case2_id,
        officer_id="OFF-001",
        officer_name="Admin Officer",
        action=AuditAction.APPROVE,
        notes="All details verified and correct.",
        timestamp=datetime.utcnow() - timedelta(days=1)
    )
    db.add(log1)
    db.commit()

    print(f"Successfully added 2 cases and 1 audit log.")
    db.close()

if __name__ == "__main__":
    seed()
