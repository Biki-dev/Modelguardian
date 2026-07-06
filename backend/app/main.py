from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.core.db import create_db_and_tables
from app.api.audits import router as audit_router


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ModelGuardian AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(health_router)
app.include_router(audit_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/")
def root():
    return {"message": "ModelGuardian AI backend is running"}