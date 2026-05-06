"""
CasePulse AI/NLP Services Package
-----------------------------------
All service classes are exported here for clean imports elsewhere:

    from app.services import PDFReader, NLPExtractor, RiskService, AuditService …
"""

from app.services.pdf_service        import PDFReader
from app.services.ocr_service        import OCRService
from app.services.extraction_service import NLPExtractor
from app.services.action_plan_service import ActionGenerator
from app.services.confidence_service  import ConfidenceService
from app.services.highlight_service   import HighlightService
from app.services.department_mapper   import DepartmentMapper
from app.services.deadline_service    import DeadlineService
from app.services.risk_service        import RiskService, AuditAction
from app.services.audit_service       import AuditService

__all__ = [
    "PDFReader",
    "OCRService",
    "NLPExtractor",
    "ActionGenerator",
    "ConfidenceService",
    "HighlightService",
    "DepartmentMapper",
    "DeadlineService",
    "RiskService",
    "AuditAction",
    "AuditService",
]
