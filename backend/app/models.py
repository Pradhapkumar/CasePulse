from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class CaseDocument(Base):
    __tablename__ = "case_documents"

    id = Column(Integer, primary_key=True, index=True)
    case_uid = Column(String, unique=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    raw_text = Column(Text)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    extracted_data = relationship("ExtractedData", back_populates="case_document", uselist=False)
    action_plan = relationship("ActionPlan", back_populates="case_document", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="case_document")

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    case_number = Column(String)
    court_name = Column(String)
    date_of_order = Column(String)
    petitioner = Column(String)
    respondent = Column(String)
    parties_involved = Column(Text)
    key_directions = Column(Text)
    timelines = Column(String)
    responsible_department = Column(String)
    important_keywords = Column(Text)
    confidence_score = Column(Integer)
    source_snippets = Column(Text)
    
    # New fields for Case Summary
    case_type = Column(String, nullable=True)
    judgment_date = Column(String, nullable=True)
    hearings_count = Column(String, nullable=True)
    legal_sections = Column(JSON, nullable=True)

    case_document = relationship("CaseDocument", back_populates="extracted_data")

class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    action_type = Column(String)
    required_action = Column(Text)
    responsible_department = Column(String)
    deadline = Column(String)
    priority = Column(String)
    risk_level = Column(String)
    reason = Column(Text)
    source_text = Column(Text)
    confidence_score = Column(Integer)
    risk_score = Column(Integer, nullable=True)
    risk_factors = Column(Text, nullable=True)
    verification_status = Column(String)
    reviewer_name = Column(String, nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    verified_at = Column(DateTime, nullable=True)

    case_document = relationship("CaseDocument", back_populates="action_plan")

class CaseSummary(Base):
    __tablename__ = "case_summaries"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    case_uid = Column(String, unique=True, index=True)
    case_title = Column(String, nullable=True)
    case_type = Column(String)
    case_number = Column(String)
    court_name = Column(String)
    judgment_date = Column(String)
    petitioner = Column(String)
    respondent = Column(String)
    hearings_count = Column(String)
    related_department = Column(String)
    action_type = Column(String)
    required_action = Column(Text)
    deadline = Column(String)
    priority = Column(String)
    risk_level = Column(String)
    confidence_score = Column(Integer)
    source_evidence = Column(Text)
    summary_text = Column(Text)
    qr_url = Column(String)
    legal_sections = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case_document = relationship("CaseDocument")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("case_documents.id"))
    action = Column(String)
    performed_by = Column(String)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    case_document = relationship("CaseDocument", back_populates="audit_logs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
