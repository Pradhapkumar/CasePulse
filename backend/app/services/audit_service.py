"""
Audit Service
-------------
Records every officer action (approve / edit / reject / view) on a case
and provides a queryable audit log.

Storage: SQLite via SQLAlchemy (reuses the app's existing database session).
If needed in the future, this can be swapped for PostgreSQL with zero changes.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from app.models import AuditLog


# ── Action constants ─────────────────────────────────────────────────────────
class AuditAction:
    VIEW    = "VIEW"
    APPROVE = "APPROVE"
    EDIT    = "EDIT"
    REJECT  = "REJECT"
    UPLOAD  = "UPLOAD"
    DELETE  = "DELETE"

    ALL = [VIEW, APPROVE, EDIT, REJECT, UPLOAD, DELETE]


class AuditService:
    """Records and retrieves officer actions on cases."""

    # ------------------------------------------------------------------ #
    #  Write operations
    # ------------------------------------------------------------------ #

    def log(
        self,
        db: Session,
        *,
        case_id: str,
        officer_id: str,
        officer_name: str,
        action: str,
        notes: Optional[str] = None,
        changed_fields: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        Write a new audit entry.

        Args:
            db            : SQLAlchemy database session (injected via FastAPI Depends).
            case_id       : ID of the case being acted upon.
            officer_id    : Unique ID of the officer performing the action.
            officer_name  : Human-readable officer name (for display).
            action        : One of AuditAction constants.
            notes         : Optional free-text remarks by the officer.
            changed_fields: Dict of field → new_value pairs when action == EDIT.

        Returns:
            The newly created AuditLog ORM object.
        """
        if action not in AuditAction.ALL:
            raise ValueError(f"Invalid audit action: '{action}'. Must be one of {AuditAction.ALL}")

        entry = AuditLog(
            case_id        = case_id,
            officer_id     = officer_id,
            officer_name   = officer_name,
            action         = action,
            notes          = notes,
            changed_fields = str(changed_fields) if changed_fields else None,
            timestamp      = datetime.utcnow(),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    # ------------------------------------------------------------------ #
    #  Read operations
    # ------------------------------------------------------------------ #

    def get_by_case(
        self,
        db: Session,
        case_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Return all audit entries for a specific case, newest first.

        Args:
            db      : SQLAlchemy session.
            case_id : Case identifier.
            limit   : Max records to return.

        Returns:
            List of serialised audit log dicts.
        """
        rows = (
            db.query(AuditLog)
            .filter(AuditLog.case_id == case_id)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [self._serialize(r) for r in rows]

    def get_by_officer(
        self,
        db: Session,
        officer_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Return all audit entries performed by a specific officer, newest first.

        Args:
            db         : SQLAlchemy session.
            officer_id : Officer identifier.
            limit      : Max records to return.

        Returns:
            List of serialised audit log dicts.
        """
        rows = (
            db.query(AuditLog)
            .filter(AuditLog.officer_id == officer_id)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [self._serialize(r) for r in rows]

    def get_recent(
        self,
        db: Session,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Return the most recent audit entries across all cases.

        Args:
            db    : SQLAlchemy session.
            limit : Max records to return.

        Returns:
            List of serialised audit log dicts.
        """
        rows = (
            db.query(AuditLog)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [self._serialize(r) for r in rows]

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _serialize(entry: AuditLog) -> Dict[str, Any]:
        """Convert an AuditLog ORM object to a plain dict for API responses."""
        return {
            "id":             entry.id,
            "case_id":        entry.case_id,
            "officer_id":     entry.officer_id,
            "officer_name":   entry.officer_name,
            "action":         entry.action,
            "notes":          entry.notes,
            "changed_fields": entry.changed_fields,
            "timestamp":      entry.timestamp.isoformat() if entry.timestamp else None,
        }
