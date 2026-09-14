"""
FastAPI application entrypoint.

Run with:  uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base, engine
from app import models  # noqa: F401  (import registers all tables on Base.metadata)
from app.api.routes import auth, users

# create_all() is fine for early development (creates tables that don't
# exist yet, never touches ones that do). Once the schema stabilizes,
# switch to Alembic migrations (already in requirements.txt) instead --
# create_all() can't handle altering an existing column/table.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAssist AI API",
    description="Informational, non-diagnostic medical report summarization and RAG chat platform.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
