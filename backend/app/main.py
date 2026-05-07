from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
import os
from .routes import upload, extraction, action_plan, verification, dashboard, cases, audit, translation, ml, auth, case_summary, search, public, legal_analyzer
from .services import auth_service
from .schemas import SignupRequest

app = FastAPI(title="CasePulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

os.makedirs("uploads/judgments", exist_ok=True)
os.makedirs("processed/extracted_text", exist_ok=True)
os.makedirs("processed/source_snippets", exist_ok=True)
os.makedirs("database", exist_ok=True)

app.include_router(upload.router)
app.include_router(extraction.router)
app.include_router(action_plan.router)
app.include_router(verification.router)
app.include_router(dashboard.router)
app.include_router(cases.router)
app.include_router(audit.router)
app.include_router(translation.router)
app.include_router(ml.router)
app.include_router(auth.router)
app.include_router(case_summary.router, prefix="/api/case-summary", tags=["Case Summary"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(public.router, prefix="/api/public", tags=["Public Case"])
app.include_router(legal_analyzer.router)

@app.get("/")
def root():
    return {
        "message": "CasePulse Backend is running",
        "docs": "/docs"
    }

from database.seed_data import seed_db
from .database import SessionLocal
db = SessionLocal()
seed_db(db)

# Seed Demo User
demo_email = "officer@casepulse.gov"
if not auth_service.get_user_by_email(db, demo_email):
    auth_service.create_user(db, SignupRequest(
        name="Legal Officer",
        email=demo_email,
        password="password123",
        role="Legal Reviewer"
    ))
db.close()
