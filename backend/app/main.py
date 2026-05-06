"""
CasePulse Backend — FastAPI Application Entry Point
=====================================================
Routes registered:
    /api/upload       → Upload PDF
    /api/extract      → AI/NLP Pipeline
    /api/action-plan  → Action Plan Generation
    /api/verify       → Officer Review (approve/edit/reject)
    /api/cases        → Case CRUD
    /api/audit        → Audit Trail
    /api/dashboard    → Dashboard Stats & Feed
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import upload, extraction, action_plan, verification, cases, audit, dashboard

# ── App instance ──────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "CasePulse API",
    description = "AI-powered court case management system for government officers.",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],   # Tighten in production
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── DB init on startup ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Create all tables if they don't exist yet."""
    init_db()

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(upload.router,       prefix="/api/upload",       tags=["Upload"])
app.include_router(extraction.router,   prefix="/api/extract",      tags=["Extraction"])
app.include_router(action_plan.router,  prefix="/api/action-plan",  tags=["Action Plan"])
app.include_router(verification.router, prefix="/api/verify",       tags=["Verification"])
app.include_router(cases.router,        prefix="/api/cases",        tags=["Cases"])
app.include_router(audit.router,        prefix="/api/audit",        tags=["Audit"])
app.include_router(dashboard.router,    prefix="/api/dashboard",    tags=["Dashboard"])

# ── Health endpoints ──────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "CasePulse API is running ✅",
        "version": "1.0.0",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


# ── Dev server ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3001, reload=True)
