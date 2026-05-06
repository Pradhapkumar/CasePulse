"""Routes package — exposes all router modules for clean imports in main.py."""

from app.routes import upload, extraction, action_plan, verification, cases, audit, dashboard

__all__ = [
    "upload",
    "extraction",
    "action_plan",
    "verification",
    "cases",
    "audit",
    "dashboard",
]
