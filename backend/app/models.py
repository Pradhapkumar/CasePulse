"""
SQLAlchemy ORM Models for CasePulse
-------------------------------------
Tables:
    cases       - Uploaded court cases
    audit_logs  - Officer action history per case
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float,
    DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


# ── Case ─────────────────────────────────────────────────────────────────────

class Case(Base):
    """Represents a single uploaded court judgment / case document."""

    __tablename__ = "cases"

    id               = Column(String,   primary_key=True, index=True)
    case_number      = Column(String,   index=True, nullable=True)
    court_name       = Column(String,   nullable=True)
    petitioner       = Column(String,   nullable=True)   # Party A
    respondent       = Column(String,   nullable=True)   # Party B
    department       = Column(String,   nullable=True)   # Detected department

    # Raw / processed text
    raw_text         = Column(Text,     nullable=True)
    directions       = Column(Text,     nullable=True)   # Court directions / orders

    # AI outputs
    action_plan      = Column(Text,     nullable=True)   # JSON string
    deadlines        = Column(Text,     nullable=True)   # JSON string
    highlights       = Column(Text,     nullable=True)   # JSON string

    # Risk & confidence
    risk_level       = Column(String,   default="Unknown")   # High / Medium / Low
    confidence_score = Column(Float,    default=0.0)
    confidence_label = Column(String,   default="Low")       # High / Medium / Low

    # Officer review status
    status           = Column(String,   default="pending")   # pending / approved / rejected
    reviewed_by      = Column(String,   nullable=True)
    review_notes     = Column(Text,     nullable=True)

    # File metadata
    file_name        = Column(String,   nullable=True)
    file_path        = Column(String,   nullable=True)
    is_scanned       = Column(Boolean,  default=False)

    # Timestamps
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    audit_logs       = relationship("AuditLog", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Case id={self.id} case_number={self.case_number} status={self.status}>"


# ── Audit Log ─────────────────────────────────────────────────────────────────

class AuditLog(Base):
    """
    Records every officer action on a case.
    Actions: VIEW | APPROVE | EDIT | REJECT | UPLOAD | DELETE
    """

    __tablename__ = "audit_logs"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    case_id        = Column(String,  ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)

    # Officer info
    officer_id     = Column(String,  nullable=False, index=True)
    officer_name   = Column(String,  nullable=False)

    # Action details
    action         = Column(String,  nullable=False)        # APPROVE / EDIT / REJECT …
    notes          = Column(Text,    nullable=True)         # Free-text officer comment
    changed_fields = Column(Text,    nullable=True)         # JSON string of edits made

    # When
    timestamp      = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    case           = relationship("Case", back_populates="audit_logs")

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} case_id={self.case_id} "
            f"action={self.action} officer={self.officer_name}>"
        )
