from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, extract, action_plan, verify, dashboard

app = FastAPI(
    title="CAsePulse API",
    description="Case management system API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(extract.router, prefix="/api/extract", tags=["extract"])
app.include_router(action_plan.router, prefix="/api/action-plan", tags=["action-plan"])
app.include_router(verify.router, prefix="/api/verify", tags=["verify"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])


@app.get("/")
async def root():
    return {
        "message": "CAsePulse API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
